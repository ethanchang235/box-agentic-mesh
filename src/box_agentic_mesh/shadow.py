"""
Shadow Box Layer.

Provides a safe staging area for autonomous file operations. Files are copied
to a `[SHADOW]` subfolder where agents can perform edits and reorganizations.
Changes are only committed to the production folder after explicit approval.

Architecture:
    Main Folder/
    ├── [SHADOW]/          # Staging area for autonomous operations
    │   ├── file1.txt     # Copies of production files
    │   └── file2.txt
    ├── production_file.txt
    └── .agent_memory.json

Usage:
    # Create staging area with all files
    shadow_id = create_shadow("folder_id")

    # Commit approved changes to production
    commit_shadow("folder_id", approval=True)
"""

import io
from boxsdk import Client, OAuth2
from .config import BOX_CLIENT_ID, BOX_CLIENT_SECRET, BOX_ACCESS_TOKEN


def get_box_client() -> Client:
    """Create and return an authenticated Box client.

    Returns:
        Authenticated Box SDK Client instance.

    Raises:
        ValueError: If BOX_ACCESS_TOKEN is not configured.
    """
    if BOX_ACCESS_TOKEN:
        oauth = OAuth2(
            client_id=BOX_CLIENT_ID,
            client_secret=BOX_CLIENT_SECRET,
            access_token=BOX_ACCESS_TOKEN,
        )
    else:
        raise ValueError("BOX_ACCESS_TOKEN required. Configure in .env file.")
    return Client(oauth)


def create_shadow(folder_id: str, file_ids: list[str] | None = None) -> str:
    """Create a Shadow Box staging subfolder.

    Creates a `[SHADOW]` subfolder in the specified folder and copies
    either the specified files or all files from the parent folder.

    Args:
        folder_id: The Box folder ID to create shadow staging in.
        file_ids: Optional list of specific file IDs to copy. If None,
                  copies all files from the parent folder.

    Returns:
        The Box folder ID of the created shadow folder.
    """
    client = get_box_client()
    folder = client.folder(folder_id)
    shadow_name = "[SHADOW]"

    shadow_folder = None
    for item in folder.get_items():
        if item.name == shadow_name and item.type == "folder":
            shadow_folder = item
            break
    if not shadow_folder:
        shadow_folder = folder.create_subfolder(shadow_name)

    if file_ids:
        for file_id in file_ids:
            file = client.file(file_id)
            file.copy(parent_folder=shadow_folder)
    else:
        for item in folder.get_items():
            if item.type == "file":
                item.copy(parent_folder=shadow_folder)

    return shadow_folder.id


def commit_shadow(folder_id: str, approval: bool = False) -> None:
    """Commit staged changes from Shadow Box to production.

    Copies files from the shadow folder to the main folder, overwriting
    existing files with the same name. The shadow folder is then deleted.

    Args:
        folder_id: The Box folder ID containing the shadow staging area.
        approval: Boolean flag requiring explicit approval before commit.
                  Set to True to actually perform the commit.
    """
    if not approval:
        print("Approval required for commit. Set approval=True to proceed.")
        return

    client = get_box_client()
    folder = client.folder(folder_id)
    shadow_name = "[SHADOW]"

    shadow_folder = None
    for item in folder.get_items():
        if item.name == shadow_name and item.type == "folder":
            shadow_folder = item
            break
    if not shadow_folder:
        print("No shadow folder found.")
        return

    for item in shadow_folder.get_items():
        if item.type == "file":
            main_file = None
            for main_item in folder.get_items():
                if main_item.name == item.name and main_item.type == "file":
                    main_file = main_item
                    break
            if main_file:
                content = item.content()
                main_file.delete()
                folder.upload_stream(io.BytesIO(content), main_file.name)
            else:
                item.copy(parent_folder=folder)

    shadow_folder.delete()
