#!/usr/bin/env python3
'''
author: Christian Olaf Häusler
created on Wednesday February 27 2020
'''


from nilearn import plotting
import matplotlib.pyplot as plt
import matplotlib as mpl
import argparse
import os


# anatImg = '/usr/share/fsl/5.0/data/standard/MNI152_T1_1mm.nii.gz'
anatImg = '/usr/share/data/fsl-mni152-templates/MNI152_T1_0.5mm.nii.gz'

# list of primary contrasts
# words > no-speech (bottom), Ne > kon (middle), Nn > kon (top image)
primCopes = ['cope1_z3.4.gfeat/cope1.feat/thresh_zstat1.nii.gz',
             'cope3_z3.4.gfeat/cope1.feat/thresh_zstat1.nii.gz',
             'cope5_z3.4.gfeat/cope1.feat/thresh_zstat1.nii.gz']

# list of corresponding reverse contrasts
# No-sp > words, Kon > ne, Kon > nn
reveCopes = ['cope2_z3.4.gfeat/cope1.feat/thresh_zstat1.nii.gz',
             'cope4_z3.4.gfeat/cope1.feat/thresh_zstat1.nii.gz',
             'cope6_z3.4.gfeat/cope1.feat/thresh_zstat1.nii.gz']


def parse_arguments():
    '''
    '''
    parser = argparse.ArgumentParser(
        description='Creates plot of three stacked thresholded zmaps'
    )

    parser.add_argument('-d',
                        default='inputs/studyforrest-speechanno-validation/3rd-lvl',
                        help='directory that contains 3rd lvl COPE directories')

    parser.add_argument('-o',
                        default='paper/figures/',
                        help='output dir for zmaps & colorbars')

    args = parser.parse_args()

    inDir = args.d
    outFile = args.o

    return inDir, outFile


def process_group_averages(outfpath, imageList=
                           ['cope1_z3.4.gfeat/cope1.feat/thresh_zstat1.nii.gz',
                            'cope3_z3.4.gfeat/cope1.feat/thresh_zstat1.nii.gz',
                            'cope3_z3.4.gfeat/cope1.feat/thresh_zstat1.nii.gz']
                           ):
    '''
    '''
    bottomImg = imageList[0]
    middleImg = imageList[1]
    topImg = imageList[2]
    print('creating plot for 3rd lvl group analysis')

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(15,15))
    plt.subplots_adjust(wspace=0, hspace=0)

    # plot axial / horizontal plane
    axis = ax1
    mode = 'z'  # axial/horizontal slice
    coord = [9]
    plot_grp_slice(mode, coord,
                   bottomImg, middleImg, topImg,
                   title='Z>3.4, p<0.05', axis=axis)

    # plot coronal plane
    axis = ax2
    mode = 'y'
    coord = [-18]
    plot_grp_slice(mode, coord,
                   bottomImg, middleImg, topImg,
                   axis=axis)

    # plot left sagittal plane
    axis = ax3
    mode = 'x'
    coord = [-55]
    plot_grp_slice(mode, coord,
                   bottomImg, middleImg, topImg,
                   axis=axis)
    # mirror horizontally
    plt.gca().invert_xaxis()

    # plot right sagittal plane
    axis = ax4
    mode = 'x'
    coord = [55]
    plot_grp_slice(mode, coord,
                   bottomImg, middleImg, topImg,
                   axis=axis)

    # manually, add a legend in bottom, right plot (right sagittal plane
    blue = mpl.patches.Patch(color='blue',
                             label='tags > no-speech')
    red = mpl.patches.Patch(color='red',
                            label='proper nouns > coord. conjunctions',)
    green = mpl.patches.Patch(color='green',
                              label='nouns > coord. conjunctions')
    plt.legend(handles=[blue, red, green], facecolor='white', framealpha=1)

    # set space between subplots and outer edge to black
    fig.patch.set_facecolor('black')
    # cut space between subplots and outer edge
    fig.patch.set_visible(False)

    # save as SVG
    svgOut = outfpath + '.svg'
    plt.savefig(svgOut,
                transparent=True,
                pad_inches=0,
                facecolor=fig.get_facecolor())

    # save as PDF
    pdfOut = outfpath + '.pdf'
    plt.savefig(pdfOut,
                transparent=True,
                pad_inches=0,
                facecolor=fig.get_facecolor())


    plt.close()


def plot_grp_slice(mode, coord,
                   bottomImg, middleImg, topImg, axis,
                   title=None, anno=True):
    '''
    '''
    display = plotting.plot_anat(anat_img=anatImg,
                                 title=title,
                                 axes=axis,
                                 annotate=anno,
                                 display_mode=mode,
                                 draw_cross=False,
                                 cut_coords=coord)

    # bottom z-map
    colorMap = plt.cm.get_cmap('Blues')
    colorMap = colorMap.reversed()
    display.add_overlay(bottomImg,
                        threshold=3.4,
                        cmap=colorMap,  # plotting.cm.black_blue,
                        vmin=3.4,
                        vmax=6.5,
                        alpha=1.0)

    # middle z-map
    colorMap = plt.cm.get_cmap('YlOrRd')
    colorMap = colorMap.reversed()
    display.add_overlay(middleImg,
                        threshold=3.4,
                        cmap=colorMap,
                        vmin=3.4,
                        vmax=6.5,
                        alpha=1.0)

    # top z-map
    colorMap = plt.cm.get_cmap('Greens')
    colorMap = colorMap.reversed()
    display.add_overlay(topImg,
                        threshold=3.4,
                        cmap=colorMap,  # plotting.cm.red_transparent,
                        vmin=3.4,
                        vmax=6.5,
                        alpha=1.0)


    return display


def plot_colorbars(outFpath):
    '''
    '''
    fig = plt.figure(figsize=(5, 1))
    gridspec = fig.add_gridspec(3, 2)
    cax1 = fig.add_subplot(gridspec[0, :])
    cax2 = fig.add_subplot(gridspec[1, :])
    cax3 = fig.add_subplot(gridspec[2, :])
    # decrease horizontal space between colorbars
    gridspec.update(left=0.01, right=0.98, top=0.97, bottom=0.23, hspace=0.15)

    # Blue colorbar
    cmap = mpl.cm.Blues
    cmap = cmap.reversed()
    norm = mpl.colors.Normalize(vmin=3.4, vmax=6.5)
    cb1 = mpl.colorbar.ColorbarBase(cax1,
                                    cmap=cmap,
                                    norm=norm,
                                    orientation='horizontal')
    cax1.tick_params(colors='w')
    plt.setp(cax1.get_xticklabels(), visible=False)
    cb1.outline.set_edgecolor('w')

    # Red colorbar
    cmap = mpl.cm.YlOrRd
    cmap = cmap.reversed()
    norm = mpl.colors.Normalize(vmin=3.4, vmax=6.5)
    cb2 = mpl.colorbar.ColorbarBase(cax2,
                                    cmap=cmap,
                                    norm=norm,
                                    orientation='horizontal')

    plt.setp(cax2.get_xticklabels(), visible=False)
    cax2.tick_params(colors='w')
    cb2.outline.set_edgecolor('w')

    # Green colorbar
    cmap = mpl.cm.Greens
    cmap = cmap.reversed()
    norm = mpl.colors.Normalize(vmin=3.4, vmax=6.5)
    cb3 = mpl.colorbar.ColorbarBase(cax3,
                                    cmap=cmap,
                                    norm=norm,
                                    orientation='horizontal')

    cax3.tick_params(colors='w')
    cb3.set_label('Z value', color='w')
    cb3.outline.set_edgecolor('w')

#    plt.tight_layout()

    # save as svg
    svgOut = outFpath + '.svg'
    plt.savefig(svgOut, transparent=True, facecolor='black')

    # save as pdf
    svgOut = outFpath + '.pdf'
    plt.savefig(svgOut, transparent=True, facecolor='black')


# main program #
if __name__ == "__main__":
    # get the command line arguments
    inDir, outDir = parse_arguments()

    inFpathes = [os.path.join(inDir, cope) for cope in primCopes]

    os.makedirs(os.path.dirname(outDir), exist_ok=True)

    # plotting stacked zmaps
    fName = 'slices'
    outFile = os.path.join(outDir, fName)
    process_group_averages(outFile, inFpathes)

    # plotting colorbars
    fName = 'colorbars'
    outFile = os.path.join(outDir, fName)
    plot_colorbars(outFile)

    plt.close('all')
