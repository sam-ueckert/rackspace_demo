import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import streamlit as st

# Assuming the functions are imported from streamlit_app.py
from streamlit_app import filter_data_center, make_reservations


class TestStreamlitApp(unittest.TestCase):

    @patch('streamlit.sidebar.selectbox')
    def test_filter_data_center(self, mock_selectbox):
        # Mock the DataFrame
        data = {
            'Data Center': ['DC1', 'DC1', 'DC2'],
            'Aggr Zone': ['Zone1', 'Zone2', 'Zone3']
        }
        df = pd.DataFrame(data)
        selected_data_center = 'DC1'
        
        # Mock the selectbox return value
        mock_selectbox.return_value = 'All'
        
        result_data_center, result_zone = filter_data_center(df, selected_data_center)
        
        self.assertEqual(result_data_center, 'DC1')
        self.assertEqual(result_zone, 'All')
        mock_selectbox.assert_called_once_with('Select an Aggr Zone Within DC1', ['All', 'Zone1', 'Zone2'], index=0)

    @patch('streamlit.write')
    def test_make_reservations(self, mock_write):
        # Mock the DataFrame
        data = {
            'Synced': [True, False]
        }
        edit_fw_df = pd.DataFrame(data)
        fw_event = MagicMock()
        fw_event.selection.rows = [1]
        
        make_reservations(edit_fw_df, fw_event)
        
        self.assertEqual(len(fw_event.selection.rows), 0)
        self.assertEqual(len(edit_fw_df), 1)
        mock_write.assert_called_once_with(
            ''''**<span style="font-size:24px;color:red;">Selected
            firewall out of sync. Wait, clear cache, and refresh.</span>**''',
            unsafe_allow_html=True
        )


if __name__ == '__main__':
    unittest.main()