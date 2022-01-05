import tensorflow as tf
import os
from miscnn.data_loading.interfaces.nifti_io \
    import NIFTI_interface
from miscnn.data_loading.data_io import Data_IO
from miscnn.processing.data_augmentation import Data_Augmentation
from miscnn.processing.subfunctions.normalization import Normalization
from miscnn.processing.subfunctions.clipping import Clipping
from miscnn.processing.subfunctions.resampling import Resampling
from miscnn.processing.preprocessor import Preprocessor
from miscnn.neural_network.model import Neural_Network
from miscnn.neural_network.metrics import dice_soft, dice_crossentropy, tversky_loss
from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.callbacks import EarlyStopping
from miscnn.evaluation.cross_validation import cross_validation

if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    # Initialize the NIfTI I/O interface and configure the images as one channel (grayscale) and three segmentation classes (background, kidney, tumor)
    interface = NIFTI_interface(pattern="case_00[0-9]*",
                                channels=1, classes=3)

    # Specify the kits19 data directory
    # data_path = "C:/Users/Dell/Documents/diplwmatikh/miscnn/data/"
    data_path = "F:/diplwmatikoula/nifti_kidney_master/"
    #data_path="F:/kits19_interpolated/data/"
    batch_path="F:/kits19_interpolated/new_batces/"
    #data_path="F:/run_test/"
    # Create the Data I/O object
    data_io = Data_IO(interface, data_path,batch_path=batch_path)
    # -------------------------------------------------------------------------------------------------------------
    sample_list = data_io.get_indiceslist()
    sample_list.sort()
    #print("All samples: " + str(sample_list))
    # -------------------------------------------------------------------------------------------------------------
    # Create and configure the Data Augmentation class
    data_aug = Data_Augmentation(cycles=2, scaling=True, rotations=True, elastic_deform=True, mirror=True,
                                 brightness=True, contrast=True, gamma=True, gaussian_noise=True)

    # -------------------------------------------------------------------------------------------------------------
    # Create a pixel value normalization Subfunction through Z-Score
    sf_normalize = Normalization(mode='z-score')
    # Create a clipping Subfunction between -79 and 304
    sf_clipping = Clipping(min=-79, max=304)
    # Create a resampling Subfunction to voxel spacing 3.22 x 1.62 x 1.62
    sf_resample = Resampling((3.22, 1.62, 1.62))

    # Assemble Subfunction classes into a list
    # Be aware that the Subfunctions will be exectued according to the list order!
    subfunctions = [sf_resample, sf_clipping, sf_normalize]

    # -----------------------------------------------------------------------------------------------------------
    # Create and configure the Preprocessor class
    pp = Preprocessor(data_io, data_aug=data_aug, batch_size=2, subfunctions=subfunctions, prepare_subfunctions=True,
                      prepare_batches=False, analysis="patchwise-crop", patch_shape=(80, 160, 160),
                      use_multiprocessing=True)

    # Adjust the patch overlap for predictions
    pp.patchwise_overlap = (40, 80, 80)

    # ------------------------------------------------------------------------------------------------------------
    # Create the Neural Network model
    model = Neural_Network(preprocessor=pp, loss=tversky_loss, metrics=[dice_soft, dice_crossentropy],
                           batch_queue_size=3, workers=3, learninig_rate=0.0001)

    # ------------------------------------------------------------------------------------------------------------
    cb_lr = ReduceLROnPlateau(monitor='loss', factor=0.1, patience=20, verbose=1, mode='min', min_delta=0.0001, cooldown=1,
                              min_lr=0.00001)
    cb_es = EarlyStopping(monitor='loss', min_delta=0, patience=150, verbose=1, mode='min')

    # ---------------------------------------------------------------------------------------------------------------

    # Exclude suspious samples from data set
    del sample_list[133]
    del sample_list[125]
    del sample_list[68]
    del sample_list[37]
    del sample_list[23]
    del sample_list[15]

    # Create the validation sample ID list
    validation_samples = sample_list[0:120]
    # Output validation samples
    #print("Validation samples: " + str(validation_samples))

    # Run cross-validation function
    cross_validation(validation_samples, model, k_fold=3, epochs=350, iterations=150,
                     evaluation_path="evaluation", draw_figures=True, callbacks=[cb_lr, cb_es])
    # --------------------------------------------------------------------------------------------------------------
