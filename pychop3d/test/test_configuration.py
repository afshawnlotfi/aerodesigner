"""
desired features of configuration:
    - once you set the configuration, every module has access
    - modify configuration
    - save configuration
    - load configuration
possible features:
    - convenience method to create temporary directories
    - convenience method to create timestamped directory
TODO:
    - should test a variety of functions that use configuration and verify that the output is different
        when using modified configuration

"""

import trimesh
import numpy as np
import tempfile
import yaml
import os

from pychop3d.configuration import Configuration
from pychop3d import bsp_tree
from pychop3d import bsp_node


def test_modify_configuration():
    """Verify that modifying the configuration modifies the behavior of the other modules. Create a tree with the
    default part and the default configuration, verify that it will fit in the printer volume, then modify the
    printer volume in the config and verify that a newly created tree will have a different n_parts objective
    """

    # Configuration.config = Configuration(os.path.join(os.path.dirname(
    #     __file__), 'test_data', "regression_config_1.yml"))

    config = Configuration.config
    mesh = trimesh.load(config.mesh, validate=True)

    # create bsp tree
    tree = bsp_tree.BSPTree(mesh)
    print(f"n parts: {tree.nodes[0].n_parts}")
    assert tree.nodes[0].n_parts == 1
    config.printer_extents = config.printer_extents / 2
    print("modified config")
    print(f"original tree n parts: {tree.nodes[0].n_parts}")
    assert tree.nodes[0].n_parts == 1
    new_tree = bsp_tree.BSPTree(mesh)
    print(f"new tree n parts: {new_tree.nodes[0].n_parts}")
    assert new_tree.nodes[0].n_parts == 2
    config.restore_defaults()


def test_load():
    """load a non-default parameter from a yaml file and verify that the config object matches
    """
    config = Configuration.config
    with tempfile.TemporaryDirectory() as tempdir:
        params = {
            'printer_extents': [1, 2, 3],
            'test_key': 'test_value'
        }
        yaml_path = os.path.join(tempdir, "test.yml")
        with open(yaml_path, 'w') as f:
            yaml.safe_dump(params, f)

        new_config = Configuration(yaml_path)
    assert isinstance(new_config.printer_extents, np.ndarray)
    assert np.all(new_config.printer_extents == np.array([1, 2, 3]))
    assert new_config.test_key == 'test_value'
    assert not hasattr(config, 'test_key')


def test_save():
    """modify the config, save it, verify that the modified values are saved and can be loaded
    """
    config = Configuration.config
    config.connector_diameter = 100
    with tempfile.TemporaryDirectory() as tempdir:
        # change directory
        config.directory = tempdir
        # save using a file name
        path = config.save("test_config.yml")
        # load the config back
        new_config = Configuration(path)

    assert new_config.connector_diameter == 100

    with tempfile.TemporaryDirectory() as tempdir:
        # change config directory
        config.directory = tempdir
        # save using cached name, should be 'test_config.yml'
        path = config.save()
        assert path == os.path.join(tempdir, 'test_config.yml')

    config.restore_defaults()


def test_functions():
    """modify the config and verify that various functions correctly use the updated version
    """
    config = Configuration.config
    mesh = trimesh.load(config.mesh, validate=True)
    print()
    # BSPNode instantiation (n_parts)
    n_parts_1 = bsp_node.BSPNode(mesh).n_parts
    config.printer_extents = np.array([20, 20, 20])
    n_parts_2 = bsp_node.BSPNode(mesh).n_parts
    assert n_parts_1 != n_parts_2
    config.restore_defaults()

    # get_planes (plane_spacing, default is )
    node = bsp_node.BSPNode(mesh)
    planes_1 = bsp_tree.get_planes(node.part, np.array([0, 1, 0]))
    config.plane_spacing /= 2
    planes_2 = bsp_tree.get_planes(node.part, np.array([0, 1, 0]))
    assert len(planes_2) > len(planes_1)
    config.restore_defaults()

    # uniform normals
    normals1 = config.normals.copy()
    config.n_theta = 10
    normals2 = config.normals.copy()
    config.n_phi = 10
    normals3 = config.normals.copy()
    assert len(normals1) < len(normals2) < len(normals3)
    config.restore_defaults()
    # etc, etc ...
