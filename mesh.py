# standard library
from typing import *
# third party
import argparse
import numpy as np
# RGBD Fusion
from modules import RGBDFusion

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rgb", type=str, required=True, help="directory to rgb images")
    parser.add_argument("--depth", type=str, required=True, help="depth directory")
    parser.add_argument("--traj", type=str, required=True, help="trajectory file")
    parser.add_argument("--depth-scale", type=float, default=1000.0, help="depth scale factor")
    parser.add_argument("--viz", type=bool, default=False, help="visualize")
    parser.add_argument("--focal", type=float, default=None, help="focal length")
    parser.add_argument("--calib", type=str, default=None, help="calib file, overwrite focal")
    parser.add_argument("--mesh", type=str, default=None, help="save mesh")

    args = parser.parse_args()

    intr, distort = None, None
    if args.calib:
        calib = np.loadtxt(args.calib)
        intr = calib[:4]
        if len(calib) > 4:
            distort = calib[4:]
    elif args.focal:
        intr = args.focal
    
    mesh = RGBDFusion.pipeline(
        image_dir=args.rgb,
        depth_dir=args.depth,
        traj_dir=args.traj,
        intrinsic=intr,
        distort=distort,
        depth_scale=args.depth_scale,
        viz=args.viz,
        mesh_save=args.mesh
    )
    
    RGBDFusion.simplify_mesh(
        mesh=mesh,
        voxel_size=0.05,
        save=args.mesh
    )