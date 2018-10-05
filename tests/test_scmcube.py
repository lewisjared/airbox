from os.path import join, isdir, isfile, splitext, dirname, abspath
from unittest.mock import patch, MagicMock


import pytest
from pytest import raises
import numpy as np
import re
import iris
from iris.exceptions import ConstraintMismatchError
from iris.analysis.cartography import DEFAULT_SPHERICAL_EARTH_RADIUS
import cf_units as unit
from pymagicc.io import MAGICCData
import pandas as pd
from pandas.testing import assert_frame_equal


from netcdf_scm.iris_cube_wrappers import _SCMCube, MarbleCMIP5Cube


TEST_DATA_ROOT_DIR = join(dirname(abspath(__file__)), "test_data")
TEST_DATA_MARBLE_CMIP5_DIR = join(TEST_DATA_ROOT_DIR, "marble_cmip5")
TEST_TAS_FILE = join(
    TEST_DATA_MARBLE_CMIP5_DIR,
    "cmip5",
    "1pctCO2",
    "Amon",
    "tas",
    "CanESM2",
    "r1i1p1",
    "tas_Amon_CanESM2_1pctCO2_r1i1p1_185001-198912.nc",
)


def get_test_cube_lon():
    lon = iris.coords.DimCoord(
        np.array([45, 135, 225, 315]),
        standard_name="longitude",
        units=unit.Unit("degrees"),
        long_name="longitude",
        var_name="lon",
        circular=True,
    )
    lon.guess_bounds()
    return lon


def get_test_cube_lat():
    lat = iris.coords.DimCoord(
        np.array([60, 0, -60]),
        standard_name="latitude",
        units=unit.Unit("degrees"),
        long_name="latitude",
        var_name="lat",
    )
    lat.guess_bounds()
    return lat


def get_test_cube_time():
    return iris.coords.DimCoord(
        np.array([365, 365 * 2, 365 * 3, 365 * 3 + 180]),
        standard_name="time",
        units=unit.Unit("days since 1850-1-1", calendar="365_day"),
        long_name="time",
        var_name="time",
    )


def get_test_cube_attributes():
    return {
        "Creator": "Blinky Bill",
        "Supervisor": "Patch",
        "attribute 3": "attribute 3",
        "attribute d": "hello, attribute d",
    }


@pytest.fixture(scope="function")
def test_cube(request):
    test_cube = request.cls.tclass()

    test_data = np.ma.masked_array(
        [
            [[0, 0.5, 1, 3], [0.0, 0.15, 0.25, 0.3], [-4, -5, -6, -7]],
            [[9, 9, 7, 6], [0, 1, 2, 3], [5, 4, 3, 2]],
            [[10, 14, 12, 13], [0, 1, 2, 3], [4.1, 5.2, 6.2, 7.3]],
            [[10, 18, 12, 13], [0, 1, 2, 3], [4.1, 5.2, 6.2, 7.3]],
        ],
        mask=False,
    )

    test_cube.cube = iris.cube.Cube(
        test_data,
        standard_name="air_temperature",
        long_name="air_temperature",
        var_name="air_temperature",
        dim_coords_and_dims=[
            (get_test_cube_time(), 0),
            (get_test_cube_lat(), 1),
            (get_test_cube_lon(), 2),
        ],
        units=unit.Unit("degC"),
        attributes=get_test_cube_attributes(),
    )

    return test_cube


@pytest.fixture(scope="function")
def test_sftlf_cube(request):
    test_sftlf_cube = request.cls.tclass()

    test_data = np.ma.masked_array(
        [[90, 49.9, 50.0, 50.1], [100, 49, 50, 51], [51, 30, 10, 0]], mask=False
    )
    test_sftlf_cube.cube = iris.cube.Cube(test_data)
    test_sftlf_cube.cube.standard_name = "land_area_fraction"

    test_sftlf_cube.cube.add_dim_coord(get_test_cube_lat(), 0)
    test_sftlf_cube.cube.add_dim_coord(get_test_cube_lon(), 1)

    return test_sftlf_cube


class TestSCMCube(object):
    tclass = _SCMCube

    @patch("netcdf_scm.iris_cube_wrappers.iris.load_cube")
    def test_load_data(self, mock_iris_load_cube, test_cube):
        tfile = "hello_world_test.nc"
        test_cube._get_file_from_load_data_args = MagicMock(return_value=tfile)

        vcons = 12.195
        test_cube._get_variable_constraint_from_load_data_args = MagicMock(
            return_value=vcons
        )

        lcube_return = 9848
        mock_iris_load_cube.return_value = lcube_return

        tkwargs = {
            "variable_name": "fco2antt",
            "modeling_realm": "Amon",
            "model": "CanESM2",
            "experiment": "1pctCO2",
        }
        test_cube.load_data(**tkwargs)

        test_cube._get_file_from_load_data_args.assert_called_with(**tkwargs)
        test_cube._get_variable_constraint_from_load_data_args.assert_called_with(
            **tkwargs
        )
        mock_iris_load_cube.assert_called_with(tfile, vcons)
        assert test_cube.cube == lcube_return

    def test_load_missing_variable_error(self, test_cube):
        tfile = TEST_TAS_FILE
        test_cube._get_file_from_load_data_args = MagicMock(return_value=tfile)

        bad_constraint = iris.Constraint(
            cube_func=(lambda c: c.var_name == np.str("misnamed_var"))
        )
        test_cube._get_variable_constraint_from_load_data_args = MagicMock(
            return_value=bad_constraint
        )

        with raises(ConstraintMismatchError, match="no cubes found"):
            test_cube.load_data(mocked_out="mocked")

    def test_get_file_from_load_data_args(self, test_cube):
        with pytest.raises(NotImplementedError):
            test_cube._get_file_from_load_data_args(a="junk")

    def test_get_variable_constraint_from_load_data_args(self, test_cube):
        if isinstance(test_cube, _SCMCube):
            with pytest.raises(NotImplementedError):
                test_cube._get_variable_constraint_from_load_data_args(a="junk")
        else:
            assert False, (
                "Overload this method in your subclass test to ensure that "
                "the return value satisfies `isinstance(return_value, "
                "iris.Constraint)`"
            )

    def test_get_data_path(self, test_cube):
        with pytest.raises(NotImplementedError):
            test_cube._get_data_path()

    def test_get_data_name(self, test_cube):
        with pytest.raises(NotImplementedError):
            test_cube._get_data_name()

    def test_get_metadata_load_arguments(self, test_cube):
        with pytest.raises(NotImplementedError):
            test_cube._get_metadata_load_arguments("junk name")

    @patch.object(tclass, "load_data")
    def test_get_metadata_cube(self, mock_load_data, test_cube):
        tvar = "tmdata_var"
        tload_arg_dict = {"Arg 1": 12, "Arg 2": "Val 2"}

        test_cube._get_metadata_load_arguments = MagicMock(return_value=tload_arg_dict)

        result = test_cube.get_metadata_cube(tvar)

        assert type(result) == type(test_cube)

        test_cube._get_metadata_load_arguments.assert_called_with(tvar)
        mock_load_data.assert_called_with(**tload_arg_dict)


    def test_get_scm_timeseries(
        self, test_sftlf_cube, test_cube
    ):
        tsftlf_cube = "mocked 124"
        tland_mask_threshold = "mocked 51"
        tareacella_cube = "mocked 4389"

        test_cubes_return = {"NH_OCEAN": 4, "SH_LAND": 12}
        test_cube.get_scm_timeseries_cubes = MagicMock(return_value=test_cubes_return)

        test_conversion_return = pd.DataFrame(data=np.array([1, 2, 3]))
        test_cube._convert_scm_timeseries_cubes_to_OpenSCMData = MagicMock(
            return_value=test_conversion_return
        )

        result = test_cube.get_scm_timeseries(
            sftlf_cube=tsftlf_cube,
            land_mask_threshold=tland_mask_threshold,
            areacella_cube=tareacella_cube,
        )

        test_cube.get_scm_timeseries_cubes.assert_called_with(
            sftlf_cube=tsftlf_cube,
            land_mask_threshold=tland_mask_threshold,
            areacella_cube=tareacella_cube,
        )
        test_cube._convert_scm_timeseries_cubes_to_OpenSCMData.assert_called_with(
            test_cubes_return
        )

        assert_frame_equal(result, test_conversion_return)

    # def test_get_scm_timeseries_cubes(self, test_cube):
    #     # get masks
    #     # loop over masks, apply to cube, store
    #     # then get_scm_masks does all the mask combinations
    #     #

    #     nh_mask_test = np.array([[False, False], [True, True]])
    #     mock_get_nh_mask.return_value = nh_mask_test
    #     land_mask_test = np.array([[False, True], [False, True]])
    #     mock_get_land_mask.return_value = land_mask_test

    #     nh_land_mask_expected = np.array([[False, True], [True, True]])
    #     sh_land_mask_expected = np.array([[True, True], [False, True]])
    #     nh_ocean_mask_expected = np.array([[True, False], [True, True]])
    #     sh_ocean_mask_expected = np.array([[True, True], [True, False]])

    #     expected = {
    #         "nh_land": nh_land_mask_expected,
    #         "sh_land": sh_land_mask_expected,
    #         "nh_ocean": nh_ocean_mask_expected,
    #         "sh_ocean": sh_ocean_mask_expected,
    #     }

    #     tlmt = 65
    #     tsftlf_data = "mocked out"
    #     result = test_cube._get_magicc_masks(
    #         sftlf_data=tsftlf_data, land_mask_threshold=tlmt
    #     )

    #     assert mock_get_land_mask.called_with(tsftlf_data, threshold=tlmt)

    #     assert isinstance(result, type(expected))
    #     for k, v in expected.items():
    #         assert (result[k] == v).all()


    # @pytest.mark.parametrize("input_format", ["nparray", "scmcube", None])
    # @pytest.mark.parametrize(
    #     "test_threshold",
    #     [(None), (0), (10), (30), (49), (49.9), (50), (50.1), (51), (60), (75), (100)],
    # )


    # perhaps this should be multiple tests, not just one...
        # setup
        # sftlf_var = "sftlf"
        # test_cube._sftlf_var_name = sftlf_var

        # test_cube.get_metadata_cube = MagicMock(return_value=test_sftlf_cube)



        # if input_format is "nparray":
        #     test_land_fraction_input = test_sftlf_cube.cube.data
        # elif input_format is "scmcube":
        #     test_land_fraction_input = test_sftlf_cube
        # else:
        #     test_land_fraction_input = None

        # # run
        # if test_threshold is None:
        #     result = test_cube.get_scm_timeseries(test_land_fraction_input)
        #     # default land fraction is 50%
        #     test_threshold = 50
        # else:

        # # prep for assertions
        # # having got the result, we can now update test_land_fraction_input
        # # for our assertions
        # if test_land_fraction_input is None:
        #     test_land_fraction_input = test_sftlf_cube

        # # assertions
        # if input_format is None:
        #     test_cube.get_metadata_cube.assert_called_with(sftlf_var)
        # else:
        #     test_cube.get_metadata_cube.assert_not_called()

    # if input_format is "nparray":
    #         # assert called with fails if you give a numpy array, it complains
    #         # about ambiguous values of truth arrays hence this is the best we
    #         # can do
    #         assert test_cube.get_scm_timeseries_cubes.call_count == 1
    #     else:
    #         test_cube.get_scm_timeseries_cubes.assert_called_with(
    #             sftlf_cube=test_sftlf_cube, land_mask_threshold=test_threshold
    #         )
