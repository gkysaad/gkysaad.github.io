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

def create_category_page(category):
    """Create a category page file if it doesn't exist."""
    # Sanitize category name for file system
    category_file_name = category.lower().replace(' ', '-')
    
    # Create categories directory if it doesn't exist
    category_dir = Path('category')
    category_dir.mkdir(exist_ok=True)
    
    # Create category page file
    category_file = category_dir / f"{category_file_name}.html"
    if not category_file.exists():
        content = f"""---
layout: category
title: "Posts in category '{category}'"
category: {category}
permalink: /category/{category_file_name}/
---"""
        with open(category_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created category page for: {category}")

def main():
    # Get all posts
    posts = glob.glob('_posts/*.md') + glob.glob('_posts/*.markdown')
    
    # Collect all unique categories
    all_categories = set()
    for post in posts:
        front_matter = extract_front_matter(post)
        if front_matter and 'categories' in front_matter:
            categories = front_matter['categories']
            if isinstance(categories, list):
                all_categories.update(categories)
            elif isinstance(categories, str):
                all_categories.add(categories)
            else:
                print(f"Warning: Unexpected categories format in {post}")
        elif front_matter and 'category' in front_matter:
            category = front_matter['category']
            if category:
                all_categories.add(category)
    
    # Create category pages
    for category in all_categories:
        create_category_page(category)
    
    print(f"Found {len(all_categories)} categories: {sorted(all_categories)}")

if __name__ == '__main__':
    main() 