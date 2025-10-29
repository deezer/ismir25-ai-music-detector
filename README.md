# AI-Music Detection

Code of our ISMIR 2025 paper "A Fourier Explanation of AI-music Artifacts" - D. Afchar, G. Meseguer Brocal, R. Hennequin.

This work was awarded best paper at ISMIR 2025! :party:

## Note on the context

The work we publish is a component that has led to putting to production an AI-Music detector at Deezer, which was announced in several press releases:
- [Deezer Just Rolled Out the World's First AI Music Tagging System - (Jun. 2025)](https://newsroom-deezer.com/2025/06/deezer-just-rolled-out-the-world-s-first-ai-music-tagging-system/)
- [Deezer launches world's first AI tagging system for music streaming - (Jun. 2025)](https://newsroom-deezer.com/2025/06/deezer-launches-worlds-first-ai-tagging-system-for-music-streaming/)
- [Deezer: 28% of all music delivered to streaming is now fully AI-generated](https://newsroom-deezer.com/2025/09/28-fully-ai-generated-music/)

Please note that, while the presented method is a component of our tool in production, there are several layers and incremental steps of our production tool that are not included in the research paper. Furthermore, we are continuously improving this tool to make it more robust and reliable.
Hence, the results of the code in this repository can significantly differ from the result of our production detector and are only aimed at reproducing the experiments presented in the paper.

## Use and patent

This work is licensed under the **CC BY-NC 4.0**.

It has led to the application for two patents in December 2024 to detect synthetic content. The code in this repository and derivatives hence can only be used for research, without commercial purpose.
For any commercial applications, please contact: `research@deezer.com`.


## Citation
If you use this work in your research, please cite 

```
@inproceedings{afchar2025fourier,
  author    = {Darius Afchar, Gabriel Meseguer‑Brocal, Kamil Akesbi and Romain Hennequin},
  title     = {A Fourier Explanation of AI‑music Artifacts},
  booktitle = {Proceedings of the International Society for Music Information Retrieval Conference (ISMIR)},
  year      = {2025},
  address   = {Daejeon, South Korea}
}
```