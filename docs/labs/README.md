# Polson–Sokolov Labs

Interactive statistics labs based on Polson and Sokolov,
*Bayes, Artificial Intelligence, and Deep Learning* (https://vsokolov.org/html/_book/).

Every page is a self-contained HTML file (no build step, no dependencies besides Google Fonts).
`index.html` is the hub; it links to the 24 lab pages in this folder.

## Publish on GitHub Pages

1. Create a new repository on GitHub (for example `labs`) and upload all files in this folder, including `.nojekyll`.
2. In the repository, open **Settings → Pages**.
3. Under **Build and deployment**, set **Source** to "Deploy from a branch", choose `main` and `/ (root)`, and save.
4. After a minute the site is live at `https://<your-username>.github.io/labs/`.

To put the labs inside an existing site instead, copy this folder into it (e.g. as `/labs/`). All links are relative.
