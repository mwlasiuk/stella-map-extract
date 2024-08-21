- Place __map.map__ file next to Python scripts.

![image](https://github.com/user-attachments/assets/b0927be1-3404-4be0-aab8-3ebc7eb497ec)

- Run:
``` sh
py make-convert.py
py make-pointcloud.py
```

This will give you files containing per pose point clouds and file with poses:

![image](https://github.com/user-attachments/assets/69da98c5-799f-4e42-b0f1-a017883da3ed)

To display poses use CloudCompare and set __trans_wc_x__, __trans_wc_y__ and __trans_wc_z__ as X, Y and Z coordinates. Ignore rest.

![image](https://github.com/user-attachments/assets/cdcf2ec0-96d2-4a19-89b0-7f1baf664cda)
![image](https://github.com/user-attachments/assets/d8676714-e611-481d-90c4-b4abb13436ec)

To display full point cloud load all __landmarks-for-keyframe-X.csv__ files in CloudCompare:

![image](https://github.com/user-attachments/assets/5f555c9a-94b5-4cdb-929f-4c103e8d2227)
