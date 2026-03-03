import os
import subprocess

from utils.common import run_command


def get_git_changes(repo_root):
    """
    Retrieve a sorted list of changed Markdown file paths in the repository
    that reside within an 'origin' directory.
    
    Parameters:
        repo_root (str): Path to the repository root directory.
    
    Returns:
        list: Sorted paths of changed Markdown files matching the criteria.
    """
    try:
        status_output = run_command("git status --porcelain", cwd=repo_root)

        changed_files = set()

        for line in status_output.split('\n'):
            if not line.strip():
                continue

            if len(line) >= 3:
                file_path = line[2:].lstrip()
            else:
                continue

            if file_path.endswith('.md'):
                norm_path = os.path.normpath(file_path)
                path_parts = norm_path.split(os.sep)

                # 경로 검증: origin 디렉토리가 첫 번째가 아닌 위치에 포함된 경로만 추가
                if len(path_parts) >= 3 and 'origin' in path_parts[1:]:
                    changed_files.add(file_path)

        return sorted(changed_files)
    except subprocess.CalledProcessError:
        print("Git 오류 발생")
        return []


def add_files_to_git(repo_root):
    """
    Add changed documentation files to the Git staging area.
    
    Parameters:
        repo_root (str): Path to the repository root directory.
    
    Returns:
        bool: True if the files were successfully added to the staging area, False otherwise.
    """
    try:
        run_command("git add versioned_docs/", cwd=repo_root)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git 파일 추가 오류 발생: {e}")
        return False
