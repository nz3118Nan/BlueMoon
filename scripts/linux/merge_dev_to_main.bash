#!/bin/bash

# Step 1: Stash current changes to keep them safe
git stash save "Temporary stash before merge operations"

# Step 2: Switch to main branch and merge dev
git checkout main
git merge dev

# Step 3: Push main to GitHub
git push origin main

# Step 4: Switch back to dev and merge main
git checkout dev
git merge main

# Step 5: Apply stashed changes back
git stash pop

echo "Merge operations completed. Your changes are preserved but not pushed." 