# Clean up directory
rm -rf dist/
# Now upload
python setup.py sdist bdist_wheel
twine upload dist/*
