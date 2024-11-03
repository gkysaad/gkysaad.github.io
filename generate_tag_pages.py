import os
import glob
import yaml
from pathlib import Path

def extract_front_matter(file_path):
    """Extract YAML front matter from a Jekyll post."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        if content.startswith('---'):
            try:
                _, front_matter, _ = content.split('---', 2)
                return yaml.safe_load(front_matter)
            except:
                print(f"Error processing front matter in {file_path}")
                return None
    return None

def create_tag_page(tag):
    """Create a tag page file if it doesn't exist."""
    # Sanitize tag name for file system
    tag_file_name = tag.lower().replace(' ', '-')
    
    # Create tag directory if it doesn't exist
    tag_dir = Path('tag')
    tag_dir.mkdir(exist_ok=True)
    
    # Create tag page file
    tag_file = tag_dir / f"{tag_file_name}.md"
    if not tag_file.exists():
        content = f"""---
layout: tag
title: "Posts tagged '{tag}'"
tag: {tag}
---"""
        with open(tag_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created tag page for: {tag}")

def main():
    # Get all posts
    posts = glob.glob('_posts/*.md') + glob.glob('_posts/*.markdown')
    
    # Collect all unique tags
    all_tags = set()
    for post in posts:
        front_matter = extract_front_matter(post)
        if front_matter and 'tags' in front_matter:
            tags = front_matter['tags']
            if isinstance(tags, list):
                all_tags.update(tags)
            elif isinstance(tags, str):
                all_tags.add(tags)
            else:
                print(f"Warning: Unexpected tags format in {post}")
    
    # Create tag pages
    for tag in all_tags:
        create_tag_page(tag)
    
    print(f"Found {len(all_tags)} tags: {sorted(all_tags)}")

if __name__ == '__main__':
    main() 