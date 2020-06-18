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

# T2* EPI group template
audioMask = 'code/grbold7Tad_brain_inMNI_12dof.nii.gz'

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

    fsize = (15, 15)
    fig = plt.figure(figsize=fsize, constrained_layout=False)

    # adjust space between subplots
    plt.subplots_adjust(wspace=0, hspace=0)

    # add the grid
    grid = fig.add_gridspec(28, 6)


    # plot axial / horizontal plane
    axis = fig.add_subplot(grid[0:12, 0:3])
    mode = 'z'  # axial/horizontal slice
    coord = [9]
    plot_grp_slice(mode, coord,
                   bottomImg, middleImg, topImg,
                   title='Z>3.4, p<0.05', axis=axis)

    # plot coronal plane
    axis = fig.add_subplot(grid[0:12, 3:])
    mode = 'y'
    coord = [-18]
    plot_grp_slice(mode, coord,
                   bottomImg, middleImg, topImg,
                   axis=axis)

    # plot left sagittal plane
    axis = fig.add_subplot(grid[12:24, 0:3])
    mode = 'x'
    coord = [-55]
    plot_grp_slice(mode, coord,
                   bottomImg, middleImg, topImg,
                   axis=axis)
    # mirror horizontally
    plt.gca().invert_xaxis()

    # plot right sagittal plane
    axis = fig.add_subplot(grid[12:24, 3:])
    mode = 'x'
    coord = [55]
    plot_grp_slice(mode, coord,
                   bottomImg, middleImg, topImg,
                   axis=axis)

    # text for z threshold and significance level
    plt.text(-330, 285,
             'Z>3.4, p<0.05',  # title=subject
             size=16,
             color='white',
             backgroundcolor='black',
             # set boxcolor and its edge to white and make transparent
             bbox=dict(facecolor=(1, 1, 1, 0), edgecolor=(1, 1, 1, 0)))

    # add the legend
    # plotting of the legend
    legendAxis = fig.add_subplot(grid[24:, :3])

    # manually, add a legend in bottom, right plot (right sagittal plane
    blue = mpl.patches.Patch(color='blue',
                             label='words > no-speech')
    red = mpl.patches.Patch(color='red',
                            label='proper nouns > coord. conjunctions',)
    green = mpl.patches.Patch(color='green',
                              label='nouns > coord. conjunctions')

    legendAxis.legend(handles=[blue, red, green],
                      loc='center',
                      facecolor='white',  # white background
                      prop={'size': 12},
                      framealpha=1)

    legendAxis.xaxis.set_visible(False)
    legendAxis.yaxis.set_visible(False)

    # plotting of the colorbars
    # blue colorbar for audio-description
    cb1Axis = fig.add_subplot(grid[24, 3:])
    cmap = mpl.cm.Blues
    cmap = cmap.reversed()
    norm = mpl.colors.Normalize(vmin=3.4, vmax=6.6)
    cb1 = mpl.colorbar.ColorbarBase(cb1Axis,
                                    cmap=cmap,
                                    norm=norm,
                                    orientation='horizontal')

    plt.setp(cb1Axis.get_xticklabels(), visible=False)
    cb1Axis.xaxis.set_visible(False)
    cb1.outline.set_edgecolor('w')

    # red colorbar for movie
    cb2Axis = fig.add_subplot(grid[25, 3:])
    cmap = mpl.cm.YlOrRd
    cmap = cmap.reversed()
    norm = mpl.colors.Normalize(vmin=3.4, vmax=6.6)
    cb2 = mpl.colorbar.ColorbarBase(cb2Axis,
                                    cmap=cmap,
                                    norm=norm,
                                    orientation='horizontal')



    # ticklabels and edge of the colorbar
    plt.setp(cb2Axis.get_xticklabels(), visible=False)
    cb2Axis.xaxis.set_visible(False)
    cb2.outline.set_edgecolor('w')

    # green colorbar
    cb3Axis = fig.add_subplot(grid[26, 3:])
    cmap = mpl.cm.Greens
    cmap = cmap.reversed()
    norm = mpl.colors.Normalize(vmin=3.4, vmax=6.6)
    cb3 = mpl.colorbar.ColorbarBase(cb3Axis,
                                    cmap=cmap,
                                    norm=norm,
                                    orientation='horizontal')

    cb3Axis.tick_params(colors='w')
    cb3.set_label('Z value', color='w')
    cb3.outline.set_edgecolor('w')

    # set space between subplots and outer edge to black
    fig.patch.set_facecolor('black')

    # save as SVG
    svgOut = outfpath + '.svg'
    plt.savefig(svgOut,
                bbox_inches='tight',
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
                   title=None, annoBool=True):
    '''
    '''
    # underlying MNI152 T1 0.5mm image
    colorMap = plt.cm.get_cmap('copper')
    display = plotting.plot_anat(anat_img=anatImg,
                                 axes=axis,
                                 # title=title,
                                 # annotate=annoBool,
                                 display_mode=mode,
                                 cmap=colorMap,
                                 draw_cross=False,
                                 cut_coords=coord)
    display.annotate(size=16)

    # brain mask 'grbold7Tad' in MNI space aligned with 12dof
    colorMap = plt.cm.get_cmap('Greys')
    colorMap = colorMap.reversed()
    display.add_overlay(audioMask,
                        cmap=colorMap,
                        vmin=0,
                        vmax=7000,  # adjust luminance to match MNI template
                        alpha=.95)

    # bottom z-map
    colorMap = plt.cm.get_cmap('Blues')
    colorMap = colorMap.reversed()
    display.add_overlay(bottomImg,
                        threshold=3.4,
                        cmap=colorMap,  # plotting.cm.black_blue,
                        vmin=3.4,
                        vmax=6.6,
                        alpha=1.0)

    # middle z-map
    colorMap = plt.cm.get_cmap('YlOrRd')
    colorMap = colorMap.reversed()
    display.add_overlay(middleImg,
                        threshold=3.4,
                        cmap=colorMap,
                        vmin=3.4,
                        vmax=6.6,
                        alpha=1.0)

    # top z-map
    colorMap = plt.cm.get_cmap('Greens')
    colorMap = colorMap.reversed()
    display.add_overlay(topImg,
                        threshold=3.4,
                        cmap=colorMap,  # plotting.cm.red_transparent,
                        vmin=3.4,
                        vmax=6.6,
                        alpha=1.0)

    return display


# main program #
if __name__ == "__main__":
    # set the background of all figures (for saving) to black
    plt.rcParams['savefig.facecolor'] = 'black'
    plt.rcParams['axes.facecolor'] = 'black'

    # get the command line arguments
    inDir, outDir = parse_arguments()

    inFpathes = [os.path.join(inDir, cope) for cope in primCopes]

    os.makedirs(os.path.dirname(outDir), exist_ok=True)

    # plotting stacked zmaps
    fName = 'slicescolorbars'
    outFile = os.path.join(outDir, fName)
    process_group_averages(outFile, inFpathes)

    plt.close('all')
