import trimesh
import pyrender
import numpy as np
import matplotlib.pyplot as plt
import os

def render_screenshots(obj_path, output_dir, image_size=(256, 256)):
    # OBJファイルの読み込み
    mesh = trimesh.load(obj_path, file_type='obj', force='mesh')

    # シーンの作成
    scene = pyrender.Scene()

    # 点光源の追加
    light_positions = [(2, 2, 2), (-2, -2, 2)]
    light_intensity = 150.0
    for pos in light_positions:
        light = pyrender.PointLight(color=np.ones(3), intensity=light_intensity)
        scene.add(light, pose=np.array([
            [1, 0, 0, pos[0]],
            [0, 1, 0, pos[1]],
            [0, 0, 1, pos[2]],
            [0, 0, 0, 1]
        ]))

    # カメラの設定
    camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0, aspectRatio=image_size[0] / image_size[1])
    cam_distance = max(mesh.extents) * 1.5
    cam_pose = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, cam_distance],  # カメラをオブジェクトの上方に配置
        [0, 0, 0, 1]
    ])
    scene.add(camera, pose=cam_pose)

    # レンダラーの作成
    r = pyrender.OffscreenRenderer(*image_size)

    # メッシュをシーンに追加
    render_mesh = pyrender.Mesh.from_trimesh(mesh)
    mesh_node = scene.add(render_mesh, pose=np.eye(4))

    # 90度ずつ回転させてスクリーンショットを撮影
    for angle in range(0, 360, 90):
        # 回転行列の生成
        rotation_matrix = trimesh.transformations.rotation_matrix(np.radians(angle), [0, 0, 1])
        scene.set_pose(mesh_node, pose=rotation_matrix)

        # シーンのレンダリングとスクリーンショットの保存
        color, _ = r.render(scene)
        plt.imshow(color)
        plt.axis('off')
        output_path = os.path.join(output_dir, f'screenshot_{angle}.png')
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
        print(f'Saved screenshot to {output_path}')


# 使用例
render_screenshots('anya.obj', 'screen')
