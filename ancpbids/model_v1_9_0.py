from .model_base import *

VERSION = '1.9.0'
SCHEMA = sys.modules[__name__]


class DatatypeEnum(DatatypeEnum):
    anat = {'value': 'anat', 'display_name': 'Anatomical Magnetic Resonance Imaging',
            'description': 'Magnetic resonance imaging sequences designed to characterize static, anatomical features.\n'}
    beh = {'value': 'beh', 'display_name': 'Behavioral Data', 'description': 'Behavioral data.\n'}
    dwi = {'value': 'dwi', 'display_name': 'Diffusion-Weighted Imaging',
           'description': 'Diffusion-weighted imaging (DWI).\n'}
    eeg = {'value': 'eeg', 'display_name': 'Electroencephalography', 'description': 'Electroencephalography'}
    fmap = {'value': 'fmap', 'display_name': 'Field maps',
            'description': 'MRI scans for estimating B0 inhomogeneity-induced distortions.\n'}
    func = {'value': 'func', 'display_name': 'Task-Based Magnetic Resonance Imaging',
            'description': 'Task (including resting state) imaging data\n'}
    ieeg = {'value': 'ieeg', 'display_name': 'Intracranial electroencephalography',
            'description': 'Intracranial electroencephalography (iEEG) or electrocorticography (ECoG) data\n'}
    meg = {'value': 'meg', 'display_name': 'Magnetoencephalography', 'description': 'Magnetoencephalography'}
    micr = {'value': 'micr', 'display_name': 'Microscopy', 'description': 'Microscopy'}
    motion = {'value': 'motion', 'display_name': 'Motion', 'description': 'Motion data from a tracking system'}
    perf = {'value': 'perf', 'display_name': 'Perfusion imaging',
            'description': 'Blood perfusion imaging data, including arterial spin labeling (ASL)\n'}
    pet = {'value': 'pet', 'display_name': 'Positron Emission Tomography',
           'description': 'Positron emission tomography data\n'}
    nirs = {'value': 'nirs', 'display_name': 'Near-Infrared Spectroscopy',
            'description': 'Near-Infrared Spectroscopy data organized around the SNIRF format'}


class ModalityEnum(ModalityEnum):
    mri = {'display_name': 'Magnetic Resonance Imaging', 'description': 'Data acquired with an MRI scanner.\n'}
    eeg = {'display_name': 'Electroencephalography', 'description': 'Data acquired with EEG.\n'}
    ieeg = {'display_name': 'Intracranial Electroencephalography', 'description': 'Data acquired with iEEG.\n'}
    meg = {'display_name': 'Magnetoencephalography', 'description': 'Data acquired with an MEG scanner.\n'}
    beh = {'display_name': 'Behavioral experiments',
           'description': 'Behavioral data acquired without accompanying neuroimaging data.\n'}
    pet = {'display_name': 'Positron Emission Tomography', 'description': 'Data acquired with PET.\n'}
    micr = {'display_name': 'Microscopy', 'description': 'Data acquired with a microscope.\n'}
    motion = {'display_name': 'Motion', 'description': 'Data acquired with Motion-Capture systems.\n'}
    nirs = {'display_name': 'Near-Infrared Spectroscopy', 'description': 'Data acquired with NIRS.'}


class SuffixEnum(SuffixEnum):
    TwoPE = {'value': '2PE', 'display_name': '2-photon excitation microscopy',
             'description': '2-photon excitation microscopy imaging data\n'}
    BF = {'value': 'BF', 'display_name': 'Bright-field microscopy',
          'description': 'Bright-field microscopy imaging data\n'}
    Chimap = {'value': 'Chimap', 'display_name': 'Quantitative susceptibility map (QSM)',
              'description': 'In parts per million (ppm).\nQSM allows for determining the underlying magnetic susceptibility of tissue\n(Chi)\n([Wang & Liu, 2014](https://doi.org/10.1002/mrm.25358)).\nChi maps are REQUIRED to use this suffix regardless of the method used to\ngenerate them.\n',
              'unit': 'ppm'}
    CARS = {'value': 'CARS', 'display_name': 'Coherent anti-Stokes Raman spectroscopy',
            'description': 'Coherent anti-Stokes Raman spectroscopy imaging data\n'}
    CONF = {'value': 'CONF', 'display_name': 'Confocal microscopy', 'description': 'Confocal microscopy imaging data\n'}
    DIC = {'value': 'DIC', 'display_name': 'Differential interference contrast microscopy',
           'description': 'Differential interference contrast microscopy imaging data\n'}
    DF = {'value': 'DF', 'display_name': 'Dark-field microscopy', 'description': 'Dark-field microscopy imaging data\n'}
    FLAIR = {'value': 'FLAIR', 'display_name': 'Fluid attenuated inversion recovery image',
             'description': 'In arbitrary units (arbitrary).\nStructural images with predominant T2 contribution (also known as T2-FLAIR),\nin which signal from fluids (for example, CSF) is nulled out by adjusting\ninversion time, coupled with notably long repetition and echo times.\n',
             'unit': 'arbitrary'}
    FLASH = {'value': 'FLASH', 'display_name': 'Fast-Low-Angle-Shot image',
             'description': 'FLASH (Fast-Low-Angle-Shot) is a vendor-specific implementation for spoiled\ngradient echo acquisition.\nIt is commonly used for rapid anatomical imaging and also for many different\nqMRI applications.\nWhen used for a single file, it does not convey any information about the\nimage contrast.\nWhen used in a file collection, it may result in conflicts across filenames of\ndifferent applications.\n**Change:** Removed from suffixes.\n'}
    FLUO = {'value': 'FLUO', 'display_name': 'Fluorescence microscopy',
            'description': 'Fluorescence microscopy imaging data\n'}
    IRT1 = {'value': 'IRT1', 'display_name': 'Inversion recovery T1 mapping',
            'description': 'The IRT1 method involves multiple inversion recovery spin-echo images\nacquired at different inversion times\n([Barral et al. 2010](https://doi.org/10.1002/mrm.22497)).\n'}
    M0map = {'value': 'M0map', 'display_name': 'Equilibrium magnetization (M0) map',
             'description': 'In arbitrary units (arbitrary).\nA common quantitative MRI (qMRI) fitting variable that represents the amount\nof magnetization at thermal equilibrium.\nM0 maps are RECOMMENDED to use this suffix if generated by qMRI applications\n(for example, variable flip angle T1 mapping).\n',
             'unit': 'arbitrary'}
    MEGRE = {'value': 'MEGRE', 'display_name': 'Multi-echo Gradient Recalled Echo',
             'description': 'Anatomical gradient echo images acquired at different echo times.\nPlease note that this suffix is not intended for the logical grouping of\nimages acquired using an Echo Planar Imaging (EPI) readout.\n'}
    MESE = {'value': 'MESE', 'display_name': 'Multi-echo Spin Echo',
            'description': 'The MESE method involves multiple spin echo images acquired at different echo\ntimes and is primarily used for T2 mapping.\nPlease note that this suffix is not intended for the logical grouping of\nimages acquired using an Echo Planar Imaging (EPI) readout.\n'}
    MP2RAGE = {'value': 'MP2RAGE', 'display_name': 'Magnetization Prepared Two Gradient Echoes',
               'description': 'The MP2RAGE method is a special protocol that collects several images at\ndifferent flip angles and inversion times to create a parametric T1map by\ncombining the magnitude and phase images\n([Marques et al. 2010](https://doi.org/10.1016/j.neuroimage.2009.10.002)).\n'}
    MPE = {'value': 'MPE', 'display_name': 'Multi-photon excitation microscopy',
           'description': 'Multi-photon excitation microscopy imaging data\n'}
    MPM = {'value': 'MPM', 'display_name': 'Multi-parametric Mapping',
           'description': 'The MPM approaches (a.k.a hMRI) involves the acquisition of highly-similar\nanatomical images that differ in terms of application of a magnetization\ntransfer RF pulse (MTon or MToff), flip angle and (optionally) echo time and\nmagnitue/phase parts\n([Weiskopf et al. 2013](https://doi.org/10.3389/fnins.2013.00095)).\nSee [here](https://owncloud.gwdg.de/index.php/s/iv2TOQwGy4FGDDZ) for\nsuggested MPM acquisition protocols.\n'}
    MTR = {'value': 'MTR', 'display_name': 'Magnetization Transfer Ratio',
           'description': 'This method is to calculate a semi-quantitative magnetization transfer ratio\nmap.\n'}
    MTRmap = {'value': 'MTRmap', 'display_name': 'Magnetization transfer ratio image',
              'description': 'In arbitrary units (arbitrary).\nMTR maps are REQUIRED to use this suffix regardless of the method used to\ngenerate them.\nMTRmap intensity values are RECOMMENDED to be represented in percentage in\nthe range of 0-100%.\n',
              'unit': 'arbitrary', 'minValue': 0, 'maxValue': 100}
    MTS = {'value': 'MTS', 'display_name': 'Magnetization transfer saturation',
           'description': 'This method is to calculate a semi-quantitative magnetization transfer\nsaturation index map.\nThe MTS method involves three sets of anatomical images that differ in terms\nof application of a magnetization transfer RF pulse (MTon or MToff) and flip\nangle ([Helms et al. 2008](https://doi.org/10.1002/mrm.21732)).\n'}
    MTVmap = {'value': 'MTVmap', 'display_name': 'Macromolecular tissue volume (MTV) image',
              'description': 'In arbitrary units (arbitrary).\nMTV maps are REQUIRED to use this suffix regardless of the method used to\ngenerate them.\n',
              'unit': 'arbitrary'}
    MTsat = {'value': 'MTsat', 'display_name': 'Magnetization transfer saturation image',
             'description': 'In arbitrary units (arbitrary).\nMTsat maps are REQUIRED to use this suffix regardless of the method used to\ngenerate them.\n',
             'unit': 'arbitrary'}
    MWFmap = {'value': 'MWFmap', 'display_name': 'Myelin water fraction image',
              'description': 'In arbitrary units (arbitrary).\nMWF maps are REQUIRED to use this suffix regardless of the method used to\ngenerate them.\nMWF intensity values are RECOMMENDED to be represented in percentage in the\nrange of 0-100%.\n',
              'unit': 'arbitrary', 'minValue': 0, 'maxValue': 100}
    NLO = {'value': 'NLO', 'display_name': 'Nonlinear optical microscopy',
           'description': 'Nonlinear optical microscopy imaging data\n'}
    OCT = {'value': 'OCT', 'display_name': 'Optical coherence tomography',
           'description': 'Optical coherence tomography imaging data\n'}
    PC = {'value': 'PC', 'display_name': 'Phase-contrast microscopy',
          'description': 'Phase-contrast microscopy imaging data\n'}
    PD = {'value': 'PD', 'display_name': 'Proton density image',
          'description': 'Ambiguous, may refer to a parametric image or to a conventional image.\n**Change:** Replaced by `PDw` or `PDmap`.\n',
          'unit': 'arbitrary'}
    PDT2 = {'value': 'PDT2', 'display_name': 'PD and T2 weighted image',
            'description': 'In arbitrary units (arbitrary).\nA two-volume 4D image, where the volumes are, respectively, PDw and T2w\nimages acquired simultaneously.\nIf separated into 3D volumes, the `PDw` and `T2w` suffixes SHOULD be used instead,\nand an acquisition entity MAY be used to distinguish the images from others with\nthe same suffix, for example, `acq-PDT2_PDw.nii` and `acq-PDT2_T2w.nii`.\n',
            'unit': 'arbitrary'}
    PDmap = {'value': 'PDmap', 'display_name': 'Proton density image',
             'description': 'In arbitrary units (arbitrary).\nPD maps are REQUIRED to use this suffix regardless of the method used to\ngenerate them.\n',
             'unit': 'arbitrary'}
    PDw = {'value': 'PDw', 'display_name': 'Proton density (PD) weighted image',
           'description': 'In arbitrary units (arbitrary).\nThe contrast of these images is mainly determined by spatial variations in\nthe spin density (1H) of the imaged specimen.\nThis contrast is achieved at short echo times and long repetition times;\nfor gradient echo, this weighting is also possible with a short TR (TR<<T1) and a small flip angle.\n',
           'unit': 'arbitrary'}
    PLI = {'value': 'PLI', 'display_name': 'Polarized-light microscopy',
           'description': 'Polarized-light microscopy imaging data\n'}
    R1map = {'value': 'R1map', 'display_name': 'Longitudinal relaxation rate image',
             'description': 'In seconds<sup>-1</sup> (1/s).\nR1 maps (R1 = 1/T1) are REQUIRED to use this suffix regardless of the method\nused to generate them.\n',
             'unit': '1/s'}
    R2map = {'value': 'R2map', 'display_name': 'True transverse relaxation rate image',
             'description': 'In seconds<sup>-1</sup> (1/s).\nR2 maps (R2 = 1/T2) are REQUIRED to use this suffix regardless of the method\nused to generate them.\n',
             'unit': '1/s'}
    R2starmap = {'value': 'R2starmap', 'display_name': 'Observed transverse relaxation rate image',
                 'description': 'In seconds<sup>-1</sup> (1/s).\nR2-star maps (R2star = 1/T2star) are REQUIRED to use this suffix regardless\nof the method used to generate them.\n',
                 'unit': '1/s'}
    RB1COR = {'value': 'RB1COR', 'display_name': 'RB1COR',
              'description': 'Low resolution images acquired by the body coil\n(in the gantry of the scanner) and the head coil using identical acquisition\nparameters to generate a combined sensitivity map as described in\n[Papp et al. (2016)](https://doi.org/10.1002/mrm.26058).\n'}
    RB1map = {'value': 'RB1map', 'display_name': 'RF receive sensitivity map',
              'description': 'In arbitrary units (arbitrary).\nRadio frequency (RF) receive (B1-) sensitivity maps are REQUIRED to use this\nsuffix regardless of the method used to generate them.\nRB1map intensity values are RECOMMENDED to be represented as percent\nmultiplicative factors such that Amplitude<sub>effective</sub> =\nB1-<sub>intensity</sub>\\*Amplitude<sub>ideal</sub>.\n',
              'unit': 'arbitrary'}
    S0map = {'value': 'S0map', 'display_name': 'Observed signal amplitude (S0) image',
             'description': 'In arbitrary units (arbitrary).\nFor a multi-echo (typically fMRI) sequence, S0 maps index the baseline signal\nbefore exponential (T2-star) signal decay.\nIn other words: the exponential of the intercept for a linear decay model\nacross log-transformed echos. For more information, please see, for example,\n[the tedana documentation](https://tedana.readthedocs.io/en/latest/\\\napproach.html#monoexponential-decay-model-fit).\nS0 maps are RECOMMENDED to use this suffix if derived from an ME-FMRI dataset.\n'}
    SEM = {'value': 'SEM', 'display_name': 'Scanning electron microscopy',
           'description': 'Scanning electron microscopy imaging data\n'}
    SPIM = {'value': 'SPIM', 'display_name': 'Selective plane illumination microscopy',
            'description': 'Selective plane illumination microscopy imaging data\n'}
    SR = {'value': 'SR', 'display_name': 'Super-resolution microscopy',
          'description': 'Super-resolution microscopy imaging data\n'}
    T1map = {'value': 'T1map', 'display_name': 'Longitudinal relaxation time image',
             'description': 'In seconds (s).\nT1 maps are REQUIRED to use this suffix regardless of the method used to\ngenerate them.\nSee [this interactive book on T1 mapping](https://qmrlab.org/t1_book/intro)\nfor further reading on T1-mapping.\n',
             'unit': 's'}
    T1rho = {'value': 'T1rho', 'display_name': 'T1 in rotating frame (T1 rho) image',
             'description': 'In seconds (s).\nT1-rho maps are REQUIRED to use this suffix regardless of the method used to\ngenerate them.\n',
             'unit': 's'}
    T1w = {'value': 'T1w', 'display_name': 'T1-weighted image',
           'description': 'In arbitrary units (arbitrary).\nThe contrast of these images is mainly determined by spatial variations in\nthe longitudinal relaxation time of the imaged specimen.\nIn spin-echo sequences this contrast is achieved at relatively short\nrepetition and echo times.\nTo achieve this weighting in gradient-echo images, again, short repetition\nand echo times are selected; however, at relatively large flip angles.\nAnother common approach to increase T1 weighting in gradient-echo images is\nto add an inversion preparation block to the beginning of the imaging\nsequence (for example, `TurboFLASH` or `MP-RAGE`).\n',
           'unit': 'arbitrary'}
    T2map = {'value': 'T2map', 'display_name': 'True transverse relaxation time image',
             'description': 'In seconds (s).\nT2 maps are REQUIRED to use this suffix regardless of the method used to\ngenerate them.\n',
             'unit': 's'}
    T2star = {'value': 'T2star', 'display_name': 'T2\\* image',
              'description': 'Ambiguous, may refer to a parametric image or to a conventional image.\n**Change:** Replaced by `T2starw` or `T2starmap`.\n',
              'anyOf': [{'unit': 'arbitrary'}, {'unit': 's'}]}
    T2starmap = {'value': 'T2starmap', 'display_name': 'Observed transverse relaxation time image',
                 'description': 'In seconds (s).\nT2-star maps are REQUIRED to use this suffix regardless of the method used to\ngenerate them.\n',
                 'unit': 's'}
    T2starw = {'value': 'T2starw', 'display_name': 'T2star weighted image',
               'description': 'In arbitrary units (arbitrary).\nThe contrast of these images is mainly determined by spatial variations in\nthe (observed) transverse relaxation time of the imaged specimen.\nIn spin-echo sequences, this effect is negated as the excitation is followed\nby an inversion pulse.\nThe contrast of gradient-echo images natively depends on T2-star effects.\nHowever, for T2-star variation to dominate the image contrast,\ngradient-echo acquisitions are carried out at long repetition and echo times,\nand at small flip angles.\n',
               'unit': 'arbitrary'}
    T2w = {'value': 'T2w', 'display_name': 'T2-weighted image',
           'description': 'In arbitrary units (arbitrary).\nThe contrast of these images is mainly determined by spatial variations in\nthe (true) transverse relaxation time of the imaged specimen.\nIn spin-echo sequences this contrast is achieved at relatively long\nrepetition and echo times.\nGenerally, gradient echo sequences are not the most suitable option for\nachieving T2 weighting, as their contrast natively depends on T2-star rather\nthan on T2.\n',
           'unit': 'arbitrary'}
    TB1AFI = {'value': 'TB1AFI', 'display_name': 'TB1AFI',
              'description': 'This method ([Yarnykh 2007](https://doi.org/10.1002/mrm.21120))\ncalculates a B1<sup>+</sup> map from two images acquired at interleaved (two)\nTRs with identical RF pulses using a steady-state sequence.\n'}
    TB1DAM = {'value': 'TB1DAM', 'display_name': 'TB1DAM',
              'description': 'The double-angle B1<sup>+</sup> method\n([Insko and Bolinger 1993](https://doi.org/10.1006/jmra.1993.1133)) is based\non the calculation of the actual angles from signal ratios,\ncollected by two acquisitions at different nominal excitation flip angles.\nCommon sequence types for this application include spin echo and echo planar\nimaging.\n'}
    TB1EPI = {'value': 'TB1EPI', 'display_name': 'TB1EPI',
              'description': 'This B1<sup>+</sup> mapping method\n([Jiru and Klose 2006](https://doi.org/10.1002/mrm.21083)) is based on two\nEPI readouts to acquire spin echo (SE) and stimulated echo (STE) images at\nmultiple flip angles in one sequence, used in the calculation of deviations\nfrom the nominal flip angle.\n'}
    TB1RFM = {'value': 'TB1RFM', 'display_name': 'TB1RFM',
              'description': 'The result of a Siemens `rf_map` product sequence.\nThis sequence produces two images.\nThe first image appears like an anatomical image and the second output is a\nscaled flip angle map.\n'}
    TB1SRGE = {'value': 'TB1SRGE', 'display_name': 'TB1SRGE',
               'description': 'Saturation-prepared with 2 rapid gradient echoes (SA2RAGE) uses a ratio of\ntwo saturation recovery images with different time delays,\nand a simulated look-up table to estimate B1+\n([Eggenschwiler et al. 2011](https://doi.org/10.1002/mrm.23145)).\nThis sequence can also be used in conjunction with MP2RAGE T1 mapping to\niteratively improve B1+ and T1 map estimation\n([Marques & Gruetter 2013](https://doi.org/10.1371/journal.pone.0069294)).\n'}
    TB1TFL = {'value': 'TB1TFL', 'display_name': 'TB1TFL',
              'description': 'The result of a Siemens `tfl_b1_map` product sequence.\nThis sequence produces two images.\nThe first image appears like an anatomical image and the second output is a\nscaled flip angle map.\n'}
    TB1map = {'value': 'TB1map', 'display_name': 'RF transmit field image',
              'description': 'In arbitrary units (arbitrary).\nRadio frequency (RF) transmit (B1+) field maps are REQUIRED to use this\nsuffix regardless of the method used to generate them.\nTB1map intensity values are RECOMMENDED to be represented as percent\nmultiplicative factors such that FlipAngle<sub>effective</sub> =\nB1+<sub>intensity</sub>\\*FlipAngle<sub>nominal</sub> .\n',
              'unit': 'arbitrary'}
    TEM = {'value': 'TEM', 'display_name': 'Transmission electron microscopy',
           'description': 'Transmission electron microscopy imaging data\n'}
    UNIT1 = {'value': 'UNIT1', 'display_name': 'Homogeneous (flat) T1-weighted MP2RAGE image',
             'description': 'In arbitrary units (arbitrary).\nUNIT1 images are REQUIRED to use this suffix regardless of the method used to\ngenerate them.\nNote that although this image is T1-weighted, regions without MR signal will\ncontain white salt-and-pepper noise that most segmentation algorithms will\nfail on.\nTherefore, it is important to dissociate it from `T1w`.\nPlease see [`MP2RAGE` specific notes](SPEC_ROOT/appendices/qmri.md#unit1-images)\nin the qMRI appendix for further information.\n'}
    VFA = {'value': 'VFA', 'display_name': 'Variable flip angle',
           'description': 'The VFA method involves at least two spoiled gradient echo (SPGR) of\nsteady-state free precession (SSFP) images acquired at different flip angles.\nDepending on the provided metadata fields and the sequence type,\ndata may be eligible for DESPOT1, DESPOT2 and their variants\n([Deoni et al. 2005](https://doi.org/10.1002/mrm.20314)).\n'}
    angio = {'value': 'angio', 'display_name': 'Angiogram',
             'description': 'Magnetic resonance angiography sequences focus on enhancing the contrast of\nblood vessels (generally arteries, but sometimes veins) against other tissue\ntypes.\n'}
    asl = {'value': 'asl', 'display_name': 'Arterial Spin Labeling',
           'description': 'The complete ASL time series stored as a 4D NIfTI file in the original\nacquisition order, with possible volume types including: control, label,\nm0scan, deltam, cbf.\n'}
    aslcontext = {'value': 'aslcontext', 'display_name': 'Arterial Spin Labeling Context',
                  'description': 'A TSV file defining the image types for volumes in an associated ASL file.\n'}
    asllabeling = {'value': 'asllabeling', 'display_name': 'ASL Labeling Screenshot',
                   'description': 'An anonymized screenshot of the planning of the labeling slab/plane\nwith respect to the imaging slab or slices.\nThis screenshot is based on DICOM macro C.8.13.5.14.\n'}
    beh = {'value': 'beh', 'display_name': 'Behavioral recording',
           'description': 'Behavioral recordings from tasks.\nThese files are similar to events files, but do not include the `"onset"` and\n`"duration"` columns that are mandatory for events files.\n'}
    blood = {'value': 'blood', 'display_name': 'Blood recording data',
             'description': 'Blood measurements of radioactivity stored in\n[tabular files](SPEC_ROOT/common-principles.md#tabular-files)\nand located in the `pet/` directory along with the corresponding PET data.\n'}
    bold = {'value': 'bold', 'display_name': 'Blood-Oxygen-Level Dependent image',
            'description': 'Blood-Oxygen-Level Dependent contrast (specialized T2\\* weighting)\n'}
    cbv = {'value': 'cbv', 'display_name': 'Cerebral blood volume image',
           'description': 'Cerebral Blood Volume contrast (specialized T2\\* weighting or difference between T1 weighted images)\n'}
    channels = {'value': 'channels', 'display_name': 'Channels File', 'description': 'Channel information.\n'}
    coordsystem = {'value': 'coordsystem', 'display_name': 'Coordinate System File',
                   'description': 'A JSON document specifying the coordinate system(s) used for the MEG, EEG,\nhead localization coils, and anatomical landmarks.\n'}
    defacemask = {'value': 'defacemask', 'display_name': 'Defacing Mask',
                  'description': 'A binary mask that was used to remove facial features from an anatomical MRI\nimage.\n'}
    dseg = {'value': 'dseg', 'display_name': 'Discrete Segmentation',
            'description': 'A discrete segmentation.\n\nThis suffix may only be used in derivative datasets.\n'}
    dwi = {'value': 'dwi', 'display_name': 'Diffusion-weighted image',
           'description': 'Diffusion-weighted imaging contrast (specialized T2 weighting).\n'}
    eeg = {'value': 'eeg', 'display_name': 'Electroencephalography',
           'description': 'Electroencephalography recording data.\n'}
    electrodes = {'value': 'electrodes', 'display_name': 'Electrodes',
                  'description': 'File that gives the location of (i)EEG electrodes.\n'}
    epi = {'value': 'epi', 'display_name': 'EPI',
           'description': 'The phase-encoding polarity (PEpolar) technique combines two or more Spin Echo\nEPI scans with different phase encoding directions to estimate the underlying\ninhomogeneity/deformation map.\n'}
    events = {'value': 'events', 'display_name': 'Events',
              'description': 'Event timing information from a behavioral task.\n'}
    fieldmap = {'value': 'fieldmap', 'display_name': 'Fieldmap',
                'description': 'Some MR schemes such as spiral-echo imaging (SEI) sequences are able to\ndirectly provide maps of the *B<sub>0</sub>* field inhomogeneity.\n'}
    headshape = {'value': 'headshape', 'display_name': 'Headshape File',
                 'description': 'The 3-D locations of points that describe the head shape and/or electrode\nlocations can be digitized and stored in separate files.\n'}
    ieeg = {'value': 'ieeg', 'display_name': 'Intracranial Electroencephalography',
            'description': 'Intracranial electroencephalography recording data.\n'}
    inplaneT1 = {'value': 'inplaneT1', 'display_name': 'Inplane T1',
                 'description': 'In arbitrary units (arbitrary).\nT1 weighted structural image matched to a functional (task) image.\n',
                 'unit': 'arbitrary'}
    inplaneT2 = {'value': 'inplaneT2', 'display_name': 'Inplane T2',
                 'description': 'In arbitrary units (arbitrary).\nT2 weighted structural image matched to a functional (task) image.\n',
                 'unit': 'arbitrary'}
    m0scan = {'value': 'm0scan', 'display_name': 'M0 image',
              'description': 'The M0 image is a calibration image, used to estimate the equilibrium\nmagnetization of blood.\n'}
    magnitude = {'value': 'magnitude', 'display_name': 'Magnitude',
                 'description': 'Field-mapping MR schemes such as gradient-recalled echo (GRE) generate a\nMagnitude image to be used for anatomical reference.\nRequires the existence of Phase, Phase-difference or Fieldmap maps.\n'}
    magnitude1 = {'value': 'magnitude1', 'display_name': 'Magnitude',
                  'description': 'Magnitude map generated by GRE or similar schemes, associated with the first\necho in the sequence.\n'}
    magnitude2 = {'value': 'magnitude2', 'display_name': 'Magnitude',
                  'description': 'Magnitude map generated by GRE or similar schemes, associated with the second\necho in the sequence.\n'}
    markers = {'value': 'markers', 'display_name': 'MEG Sensor Coil Positions',
               'description': 'Another manufacturer-specific detail pertains to the KIT/Yokogawa/Ricoh\nsystem, which saves the MEG sensor coil positions in a separate file with two\npossible filename extensions  (`.sqd`, `.mrk`).\nFor these files, the `markers` suffix MUST be used.\nFor example: `sub-01_task-nback_markers.sqd`\n'}
    mask = {'value': 'mask', 'display_name': 'Binary Mask',
            'description': 'A binary mask that functions as a discrete "label" for a single structure.\n\nThis suffix may only be used in derivative datasets.\n'}
    meg = {'value': 'meg', 'display_name': 'Magnetoencephalography',
           'description': 'Unprocessed MEG data stored in the native file format of the MEG instrument\nwith which the data was collected.\n'}
    motion = {'value': 'motion', 'display_name': 'Motion',
              'description': 'Data recorded from a tracking system store.\n'}
    nirs = {'value': 'nirs', 'display_name': 'Near Infrared Spectroscopy',
            'description': 'Data associated with a Shared Near Infrared Spectroscopy Format file.'}
    optodes = {'value': 'optodes', 'display_name': 'Optodes',
               'description': 'Either a light emitting device, sometimes called a transmitter, or a photoelectric transducer, sometimes called a\nreceiver.\n'}
    pet = {'value': 'pet', 'display_name': 'Positron Emission Tomography',
           'description': 'PET imaging data SHOULD be stored in 4D\n(or 3D, if only one volume was acquired) NIfTI files with the `_pet` suffix.\nVolumes MUST be stored in chronological order\n(the order they were acquired in).\n'}
    phase = {'value': 'phase', 'display_name': 'Phase image',
             'description': '[DEPRECATED](SPEC_ROOT/common-principles.md#definitions).\nPhase information associated with magnitude information stored in BOLD\ncontrast.\nThis suffix should be replaced by the\n[`part-phase`](SPEC_ROOT/appendices/entities.md#part)\nin conjunction with the `bold` suffix.\n',
             'anyOf': [{'unit': 'arbitrary'}, {'unit': 'rad'}]}
    phase1 = {'value': 'phase1', 'display_name': 'Phase',
              'description': 'Phase map generated by GRE or similar schemes, associated with the first\necho in the sequence.\n'}
    phase2 = {'value': 'phase2', 'display_name': 'Phase',
              'description': 'Phase map generated by GRE or similar schemes, associated with the second\necho in the sequence.\n'}
    phasediff = {'value': 'phasediff', 'display_name': 'Phase-difference',
                 'description': 'Some scanners subtract the `phase1` from the `phase2` map and generate a\nunique `phasediff` file.\nFor instance, this is a common output for the built-in fieldmap sequence of\nSiemens scanners.\n'}
    photo = {'value': 'photo', 'display_name': 'Photo File',
             'description': 'Photos of the anatomical landmarks, head localization coils or tissue sample.\n'}
    physio = {'value': 'physio', 'display_name': 'Physiological recording',
              'description': 'Physiological recordings such as cardiac and respiratory signals.\n'}
    probseg = {'value': 'probseg', 'display_name': 'Probabilistic Segmentation',
               'description': 'A probabilistic segmentation.\n\nThis suffix may only be used in derivative datasets.\n'}
    sbref = {'value': 'sbref', 'display_name': 'Single-band reference image',
             'description': 'Single-band reference for one or more multi-band `dwi` images.\n'}
    scans = {'value': 'scans', 'display_name': 'Scans file',
             'description': 'The purpose of this file is to describe timing and other properties of each imaging acquisition\nsequence (each run file) within one session.\nEach neural recording file SHOULD be described by exactly one row. Some recordings consist of\nmultiple parts, that span several files, for example through echo-, part-, or split- entities.\nSuch recordings MUST be documented with one row per file.\nRelative paths to files should be used under a compulsory filename header.\nIf acquisition time is included it should be listed under the acq_time header.\nAcquisition time refers to when the first data point in each run was acquired.\nFurthermore, if this header is provided, the acquisition times of all files that belong to a\nrecording MUST be identical.\nDatetime should be expressed as described in Units.\nAdditional fields can include external behavioral measures relevant to the scan.\nFor example vigilance questionnaire score administered after a resting state scan.\nAll such included additional fields SHOULD be documented in an accompanying _scans.json file\nthat describes these fields in detail (see Tabular files).\n'}
    sessions = {'value': 'sessions', 'display_name': 'Sessions file',
                'description': 'In case of multiple sessions there is an option of adding additional sessions.tsv files\ndescribing variables changing between sessions.\nIn such case one file per participant SHOULD be added.\nThese files MUST include a session_id column and describe each session by one and only one row.\nColumn names in sessions.tsv files MUST be different from group level participant key column\nnames in the participants.tsv file.\n'}
    stim = {'value': 'stim', 'display_name': 'Continuous recording',
            'description': 'Continuous measures, such as parameters of a film or audio stimulus.\n'}
    uCT = {'value': 'uCT', 'display_name': 'Micro-CT', 'description': 'Micro-CT imaging data\n'}


class EntityEnum(EntityEnum):
    subject = {'name': 'sub', 'display_name': 'Subject',
               'description': 'A person or animal participating in the study.\n', 'type': 'string', 'format': 'label'}
    session = {'name': 'ses', 'display_name': 'Session',
               'description': "A logical grouping of neuroimaging and behavioral data consistent across subjects.\nSession can (but doesn't have to) be synonymous to a visit in a longitudinal study.\nIn general, subjects will stay in the scanner during one session.\nHowever, for example, if a subject has to leave the scanner room and then\nbe re-positioned on the scanner bed, the set of MRI acquisitions will still\nbe considered as a session and match sessions acquired in other subjects.\nSimilarly, in situations where different data types are obtained over\nseveral visits (for example fMRI on one day followed by DWI the day after)\nthose can be grouped in one session.\n\nDefining multiple sessions is appropriate when several identical or similar\ndata acquisitions are planned and performed on all -or most- subjects,\noften in the case of some intervention between sessions\n(for example, training).\n",
               'type': 'string', 'format': 'label'}
    sample = {'name': 'sample', 'display_name': 'Sample',
              'description': 'A sample pertaining to a subject such as tissue, primary cell or cell-free sample.\nThe `sample-<label>` entity is used to distinguish between different samples from the same subject.\nThe label MUST be unique per subject and is RECOMMENDED to be unique throughout the dataset.\n',
              'type': 'string', 'format': 'label'}
    task = {'name': 'task', 'display_name': 'Task',
            'description': 'A set of structured activities performed by the participant.\nTasks are usually accompanied by stimuli and responses, and can greatly vary in complexity.\n\nIn the context of brain scanning, a task is always tied to one data acquisition.\nTherefore, even if during one acquisition the subject performed multiple conceptually different behaviors\n(with different sets of instructions) they will be considered one (combined) task.\n\nWhile tasks may be repeated across multiple acquisitions,\na given task may have different sets of stimuli (for example, randomized order) and participant responses\nacross subjects, sessions, and runs.\n\nThe `task-<label>` MUST be consistent across subjects and sessions.\n\nFiles with the `task-<label>` entity SHOULD have an associated\n[events file](SPEC_ROOT/modality-specific-files/task-events.md#task-events),\nas well as certain metadata fields in the associated JSON file.\n\nFor the purpose of this specification we consider the so-called "resting state" a task,\nalthough events files are not expected for resting state data.\nAdditionally, a common convention in the specification is to include the word "rest" in\nthe `task` label for resting state files (for example, `task-rest`).\n',
            'type': 'string', 'format': 'label'}
    tracksys = {'name': 'tracksys', 'display_name': 'Tracking system',
                'description': 'The `tracksys-<label>` entity can be used as a key-value pair\nto label *_motion.tsv and *_motion.json files.\nIt can also be used to label *_channel.tsv or *_events.tsv files\nwhen they belong to a specific tracking system.\n\nThis entity corresponds to the `"TrackingSystemName"` metadata field in a *_motion.json file.\n`tracksys-<label>` entity is a concise string whereas `"TrackingSystemName"`\nmay be longer and more human readable.\n',
                'type': 'string', 'format': 'label'}
    acquisition = {'name': 'acq', 'display_name': 'Acquisition',
                   'description': 'The `acq-<label>` entity corresponds to a custom label the user MAY use to distinguish\na different set of parameters used for acquiring the same modality.\n\nFor example, this should be used when a study includes two T1w images -\none full brain low resolution and one restricted field of view but high resolution.\nIn such case two files could have the following names:\n`sub-01_acq-highres_T1w.nii.gz` and `sub-01_acq-lowres_T1w.nii.gz`;\nhowever, the user is free to choose any other label than `highres` and `lowres` as long\nas they are consistent across subjects and sessions.\n\nIn case different sequences are used to record the same modality\n(for example, `RARE` and `FLASH` for T1w)\nthis field can also be used to make that distinction.\nThe level of detail at which the distinction is made\n(for example, just between `RARE` and `FLASH`, or between `RARE`, `FLASH`, and `FLASHsubsampled`)\nremains at the discretion of the researcher.\n',
                   'type': 'string', 'format': 'label'}
    ceagent = {'name': 'ce', 'display_name': 'Contrast Enhancing Agent',
               'description': 'The `ce-<label>` entity can be used to distinguish sequences using different contrast enhanced images.\nThe label is the name of the contrast agent.\n\nThis entity represents the `"ContrastBolusIngredient"` metadata field.\nTherefore, if the `ce-<label>` entity is present in a filename,\n`"ContrastBolusIngredient"` MAY also be added in the JSON file, with the same label.\n',
               'type': 'string', 'format': 'label'}
    tracer = {'name': 'trc', 'display_name': 'Tracer',
              'description': 'The `trc-<label>` entity can be used to distinguish sequences using different tracers.\n\nThis entity represents the `"TracerName"` metadata field.\nTherefore, if the `trc-<label>` entity is present in a filename,\n`"TracerName"` MUST be defined in the associated metadata.\nPlease note that the `<label>` does not need to match the actual value of the field.\n',
              'type': 'string', 'format': 'label'}
    stain = {'name': 'stain', 'display_name': 'Stain',
             'description': 'The `stain-<label>` key/pair values can be used to distinguish image files\nfrom the same sample using different stains or antibodies for contrast enhancement.\n\nThis entity represents the `"SampleStaining"` metadata field.\nTherefore, if the `stain-<label>` entity is present in a filename,\n`"SampleStaining"` SHOULD be defined in the associated metadata,\nalthough the label may be different.\n\nDescriptions of antibodies SHOULD also be indicated in the `"SamplePrimaryAntibodies"`\nand/or `"SampleSecondaryAntibodies"` metadata fields, as appropriate.\n',
             'type': 'string', 'format': 'label'}
    reconstruction = {'name': 'rec', 'display_name': 'Reconstruction',
                      'description': 'The `rec-<label>` entity can be used to distinguish different reconstruction algorithms\n(for example, `MoCo` for the ones using motion correction).\n',
                      'type': 'string', 'format': 'label'}
    direction = {'name': 'dir', 'display_name': 'Phase-Encoding Direction',
                 'description': 'The `dir-<label>` entity can be set to an arbitrary alphanumeric label\n(for example, `dir-LR` or `dir-AP`)\nto distinguish different phase-encoding directions.\n\nThis entity represents the `"PhaseEncodingDirection"` metadata field.\nTherefore, if the `dir-<label>` entity is present in a filename,\n`"PhaseEncodingDirection"` MUST be defined in the associated metadata.\nPlease note that the `<label>` does not need to match the actual value of the field.\n',
                 'type': 'string', 'format': 'label'}
    run = {'name': 'run', 'display_name': 'Run',
           'description': 'The `run-<index>` entity is used to distinguish separate data acquisitions with the same acquisition parameters\nand (other) entities.\n\nIf several data acquisitions (for example, MRI scans or EEG recordings)\nwith the same acquisition parameters are acquired in the same session,\nthey MUST be indexed with the [`run-<index>`](SPEC_ROOT/appendices/entities.md#run) entity:\n`_run-1`, `_run-2`, `_run-3`, and so on\n(only nonnegative integers are allowed as run indices).\n\nIf different entities apply,\nsuch as a different session indicated by [`ses-<label>`][SPEC_ROOT/appendices/entities.md#ses),\nor different acquisition parameters indicated by\n[`acq-<label>`](SPEC_ROOT/appendices/entities.md#acq),\nthen `run` is not needed to distinguish the scans and MAY be omitted.\n',
           'type': 'string', 'format': 'index'}
    modality = {'name': 'mod', 'display_name': 'Corresponding Modality',
                'description': 'The `mod-<label>` entity corresponds to modality label for defacing\nmasks, for example, T1w, inplaneT1, referenced by a defacemask image.\nFor example, `sub-01_mod-T1w_defacemask.nii.gz`.\n',
                'type': 'string', 'format': 'label'}
    echo = {'name': 'echo', 'display_name': 'Echo',
            'description': 'If files belonging to an entity-linked file collection are acquired at different\necho times, the `echo-<index>` entity MUST be used to distinguish individual files.\n\nThis entity represents the `"EchoTime"` metadata field.\nTherefore, if the `echo-<index>` entity is present in a filename,\n`"EchoTime"` MUST be defined in the associated metadata.\nPlease note that the `<index>` denotes the number/index (in the form of a nonnegative integer),\nnot the `"EchoTime"` value of the separate JSON file.\n',
            'type': 'string', 'format': 'index'}
    flip = {'name': 'flip', 'display_name': 'Flip Angle',
            'description': 'If files belonging to an entity-linked file collection are acquired at different\nflip angles, the `_flip-<index>` entity pair MUST be used to distinguish\nindividual files.\n\nThis entity represents the `"FlipAngle"` metadata field.\nTherefore, if the `flip-<index>` entity is present in a filename,\n`"FlipAngle"` MUST be defined in the associated metadata.\nPlease note that the `<index>` denotes the number/index (in the form of a nonnegative integer),\nnot the `"FlipAngle"` value of the separate JSON file.\n',
            'type': 'string', 'format': 'index'}
    inversion = {'name': 'inv', 'display_name': 'Inversion Time',
                 'description': 'If files belonging to an entity-linked file collection are acquired at different inversion times,\nthe `inv-<index>` entity MUST be used to distinguish individual files.\n\nThis entity represents the `"InversionTime` metadata field.\nTherefore, if the `inv-<index>` entity is present in a filename,\n`"InversionTime"` MUST be defined in the associated metadata.\nPlease note that the `<index>` denotes the number/index (in the form of a nonnegative integer),\nnot the `"InversionTime"` value of the separate JSON file.\n',
                 'type': 'string', 'format': 'index'}
    mtransfer = {'name': 'mt', 'display_name': 'Magnetization Transfer',
                 'description': 'If files belonging to an entity-linked file collection are acquired at different\nmagnetization transfer (MT) states, the `_mt-<label>` entity MUST be used to\ndistinguish individual files.\n\nThis entity represents the `"MTState"` metadata field.\nTherefore, if the `mt-<label>` entity is present in a filename,\n`"MTState"` MUST be defined in the associated metadata.\nAllowed label values for this entity are `on` and `off`,\nfor images acquired in presence and absence of an MT pulse, respectively.\n',
                 'type': 'string', 'format': 'label', 'enum': ['on', 'off']}
    part = {'name': 'part', 'display_name': 'Part',
            'description': 'This entity is used to indicate which component of the complex\nrepresentation of the MRI signal is represented in voxel data.\nThe `part-<label>` entity is associated with the DICOM Tag\n`0008, 9208`.\nAllowed label values for this entity are `phase`, `mag`, `real` and `imag`,\nwhich are typically used in `part-mag`/`part-phase` or\n`part-real`/`part-imag` pairs of files.\n\nPhase images MAY be in radians or in arbitrary units.\nThe sidecar JSON file MUST include the `"Units"` of the `phase` image.\nThe possible options are `"rad"` or `"arbitrary"`.\n\nWhen there is only a magnitude image of a given type, the `part` entity MAY be\nomitted.\n',
            'type': 'string', 'format': 'label', 'enum': ['mag', 'phase', 'real', 'imag']}
    processing = {'name': 'proc', 'display_name': 'Processed (on device)',
                  'description': "The proc label is analogous to rec for MR and denotes a variant of\na file that was a result of particular processing performed on the device.\n\nThis is useful for files produced in particular by Neuromag/Elekta/MEGIN's\nMaxFilter (for example, `sss`, `tsss`, `trans`, `quat` or `mc`),\nwhich some installations impose to be run on raw data because of active\nshielding software corrections before the MEG data can actually be\nexploited.\n",
                  'type': 'string', 'format': 'label'}
    hemisphere = {'name': 'hemi', 'display_name': 'Hemisphere',
                  'description': 'The `hemi-<label>` entity indicates which hemibrain is described by the file.\nAllowed label values for this entity are `L` and `R`, for the left and right\nhemibrains, respectively.\n',
                  'type': 'string', 'format': 'label', 'enum': ['L', 'R']}
    space = {'name': 'space', 'display_name': 'Space',
             'description': 'The `space-<label>` entity can be used to indicate the way in which electrode positions are interpreted\n(for EEG/MEG/iEEG data)\nor the spatial reference to which a file has been aligned (for MRI data).\nThe `<label>` MUST be taken from one of the modality specific lists in the\n[Coordinate Systems Appendix](SPEC_ROOT/appendices/coordinate-systems.md).\nFor example, for iEEG data, the restricted keywords listed under\n[iEEG Specific Coordinate Systems](SPEC_ROOT/appendices/coordinate-systems.md#ieeg-specific-coordinate-systems)\nare acceptable for `<label>`.\n\nFor EEG/MEG/iEEG data, this entity can be applied to raw data,\nbut for other data types, it is restricted to derivative data.\n',
             'type': 'string', 'format': 'label'}
    split = {'name': 'split', 'display_name': 'Split',
             'description': 'In the case of long data recordings that exceed a file size of 2Gb,\n`.fif` files are conventionally split into multiple parts.\nEach of these files has an internal pointer to the next file.\nThis is important when renaming these split recordings to the BIDS convention.\n\nInstead of a simple renaming, files should be read in and saved under their\nnew names with dedicated tools like [MNE-Python](https://mne.tools/),\nwhich will ensure that not only the filenames, but also the internal file pointers, will be updated.\n\nIt is RECOMMENDED that `.fif` files with multiple parts use the `split-<index>` entity to indicate each part.\nIf there are multiple parts of a recording and the optional `scans.tsv` is provided,\nall files MUST be listed separately in `scans.tsv` and\nthe entries for the `acq_time` column in `scans.tsv` MUST all be identical,\nas described in [Scans file](SPEC_ROOT/modality-agnostic-files.md#scans-file).\n',
             'type': 'string', 'format': 'index'}
    recording = {'name': 'recording', 'display_name': 'Recording',
                 'description': 'The `recording-<label>` entity can be used to distinguish continuous recording files.\n\nThis entity is commonly applied when continuous recordings have different sampling frequencies or start times.\nFor example, physiological recordings with different sampling frequencies may be distinguished using\nlabels like `recording-100Hz` and `recording-500Hz`.\n',
                 'type': 'string', 'format': 'label'}
    chunk = {'name': 'chunk', 'display_name': 'Chunk',
             'description': 'The `chunk-<index>` key/value pair is used to distinguish between images of\nthe same physical sample with different fields of view acquired in the same\nimaging experiment.\nThis entity applies to collections of 2D images, 3D volumes or 4D volume series\n(for example, diffusion weighted images), and may be used to indicate different\nanatomical structures or regions of the same structure.\n',
             'type': 'string', 'format': 'index'}
    segmentation = {'name': 'seg', 'display_name': 'Segmentation',
                    'description': 'The `seg-<label>` key/value pair corresponds to a custom label the user\nMAY use to distinguish different segmentations.\n\nThis entity is only applicable to derivative data.\n',
                    'type': 'string', 'format': 'label'}
    resolution = {'name': 'res', 'display_name': 'Resolution',
                  'description': 'Resolution of regularly sampled N-dimensional data.\n\nThis entity represents the `"Resolution"` metadata field.\nTherefore, if the `res-<label>` entity is present in a filename,\n`"Resolution"` MUST also be added in the JSON file, to provide interpretation.\n\nThis entity is only applicable to derivative data.\n',
                  'type': 'string', 'format': 'label'}
    density = {'name': 'den', 'display_name': 'Density',
               'description': 'Density of non-parametric surfaces.\n\nThis entity represents the `"Density"` metadata field.\nTherefore, if the `den-<label>` entity is present in a filename,\n`"Density"` MUST also be added in the JSON file, to provide interpretation.\n\nThis entity is only applicable to derivative data.\n',
               'type': 'string', 'format': 'label'}
    label = {'name': 'label', 'display_name': 'Label',
             'description': 'Tissue-type label, following a prescribed vocabulary.\nApplies to binary masks and probabilistic/partial volume segmentations\nthat describe a single tissue type.\n\nThis entity is only applicable to derivative data.\n',
             'type': 'string', 'format': 'label'}
    description = {'name': 'desc', 'display_name': 'Description',
                   'description': 'When necessary to distinguish two files that do not otherwise have a\ndistinguishing entity, the `desc-<label>` entity SHOULD be used.\n\nThis entity is only applicable to derivative data.\n',
                   'type': 'string', 'format': 'label'}
