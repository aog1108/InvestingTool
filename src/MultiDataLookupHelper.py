from LookupHelper import *


def get_accumulation_candle(high_data, low_data, volume_data, high_minus_low_cutoff, volume_return_cutoff):
    high_minus_low = (high_data - low_data) / low_data
    volume_return = get_return(volume_data, 1)

    boolean1 = high_minus_low >= high_minus_low_cutoff
    boolean2 = volume_return >= volume_return_cutoff

    return np.logical_and(boolean1[1:, :], boolean2).astype(int)
