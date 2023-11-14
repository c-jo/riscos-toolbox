"""
Python constants.
"""


class ActionbuttonConstants(object):

    # .Bits
    ActionButton_SelectedAdjust = (1<<0)
    ActionButton_SelectedSelect = (1<<2)
    ActionButton_SelectedDefault = (1<<3)
    ActionButton_SelectedCancel = (1<<4)
    ActionButton_SelectedLocal = (1<<5)
    Action_ActionButtonSelected = 534657

    # Gadget_Flags
    ActionButton_IsDefault = (1<<0)
    ActionButton_IsCancel = (1<<1)
    ActionButton_IsLocal = (1<<2)
    ActionButton_IsMenu = (1<<3)

    # Toolbox_Class
    Class_ActionButton = 128


class AdjusterConstants(object):

    # .Bits
    Action_AdjusterClicked = 534668

    # Gadget_Flags
    Adjuster_Decrement = (1<<0)
    Adjuster_Vertical = (1<<1)

    # Toolbox_Class
    Class_Adjuster = 768


class ButtonConstants(object):

    # .Bits
    Button_TaskSpriteArea = (1<<0)
    Button_AllowMenuClicks = (1<<1)

    # Toolbox_Class
    Class_Button = 960


class ColourdboxConstants(object):

    # .Bits
    Action_ColourDboxAboutToBeShown = 534976
    Action_ColourDboxDialogueCompleted = 534977
    Action_ColourDboxColourSelected = 534978
    Error_ColourDboxTasksActive = 0x80ae00
    Error_ColourDboxAllocFailed = 0x80ae01
    Error_ColourDboxShortBuffer = 0x80ae02
    Error_ColourDboxNoSuchTask = 0x80ae11
    Error_ColourDboxNoSuchMethod = 0x80ae12
    Error_ColourDboxNoSuchMiscOpMethod = 0x80ae13

    # ColourDbox_ColourFlags
    ColourDbox_ColourTransparent = (1<<0)

    # ColourDbox_DialogueCompletedFlags
    ColourDbox_DialogueCompletedColourChoice = (1<<0)

    # ColourDbox_Flags
    ColourDbox_GenerateAboutToBeShown = (1<<0)
    ColourDbox_GenerateDialogueCompleted = (1<<1)
    ColourDbox_IncludeNoneButton = (1<<2)
    ColourDbox_SelectNoneButton = (1<<3)

    # Toolbox_Class
    Class_ColourDbox = 534976


class ColourmenuConstants(object):

    # .Bits
    Action_ColourMenuAboutToBeShown = 534912
    Action_ColourMenuDialogueCompleted = 534913
    Action_ColourMenuSelection = 534914
    Error_ColourMenuTasksActive = 0x80b000
    Error_ColourMenuAllocFailed = 0x80b001
    Error_ColourMenuShortBuffer = 0x80b002
    Error_ColourMenuNoSuchTask = 0x80b011
    Error_ColourMenuNoSuchMethod = 0x80b012
    Error_ColourMenuNoSuchMiscOpMethod = 0x80b013

    # ColourMenu_Colour
    ColourMenu_None = -1
    ColourMenu_Transparent = 16

    # ColourMenu_Flags
    ColourMenu_GenerateAboutToBeShown = (1<<0)
    ColourMenu_GenerateDialogueCompleted = (1<<1)
    ColourMenu_NoneEntry = (1<<2)

    # Toolbox_Class
    Class_ColourMenu = 534912


class DcsConstants(object):

    # .Bits
    Action_DCSAboutToBeShown = 535168
    Action_DCSDiscard = 535169
    Action_DCSSave = 535170
    Action_DCSDialogueCompleted = 535171
    Action_DCSCancel = 535172
    DCS_NoMemory = 8433921
    DCS_TasksActive = 8433922

    # DCS_Flags
    DCS_GenerateAboutToBeShown = (1<<0)
    DCS_GenerateDialogueCompleted = (1<<1)

    # Toolbox_C
    DCS_FileIcon = 8562688
    DCS_Discard = 8562689
    DCS_Cancel = 8562690
    DCS_Save = 8562691

    # Toolbox_Class
    Class_DCS = 535168


class DdeutilsConstants(object):

    # .Bits
    Error_DDEUtilsUnknownSWI = 0x20600
    Error_DDEUtilsNoCLIBuffer = 0x20601
    Error_DDEUtilsNotDesktop = 0x20602
    Error_DDEUtilsNoTask = 0x20603
    Error_DDEUtilsAlreadyRegistered = 0x20604
    Error_DDEUtilsNotRegistered = 0x20605
    Message_DDEUtilsThrowbackStart = 0x42580
    Message_DDEUtilsProcessingFile = 0x42581
    Message_DDEUtilsErrorsIn = 0x42582
    Message_DDEUtilsErrorDetails = 0x42583
    Message_DDEUtilsThrowbackEnd = 0x42584
    Message_DDEUtilsInfoForFile = 0x42585
    Message_DDEUtilsInfoDetails = 0x42586

    # .Int
    DDEUtils_SeverityError = 1
    DDEUtils_SeveritySeriousError = 2
    DDEUtils_SeverityWarning = 0
    DDEUtils_ThrowbackErrorDetails = 1
    DDEUtils_ThrowbackInfoDetails = 2
    DDEUtils_ThrowbackProcessing = 0


class DisplayfieldConstants(object):

    # Gadget_Flags
    DisplayField_RJustified = (1<<1)
    DisplayField_HCentred = (1<<2)

    # Toolbox_Class
    Class_DisplayField = 448


class DraganobjectConstants(object):

    # .Bits
    DragAnObject_VPosBottom = 0
    DragAnObject_NoBound = 0
    DragAnObject_BoundObject = 0
    DragAnObject_SWIFunction = 0
    DragAnObject_HPosLeft = 0
    DragAnObject_HPosCentre = (1<<0)
    DragAnObject_HPosRight = (1<<1)
    DragAnObject_VPosCentre = (1<<2)
    DragAnObject_VPosTop = (1<<3)
    DragAnObject_BoundToWindow = (1<<4)
    DragAnObject_GivenBBox = (1<<5)
    DragAnObject_BoundPointer = (1<<6)
    DragAnObject_DropShadow = (1<<7)
    DragAnObject_NoDither = (1<<8)
    DragAnObject_CallFunction = (1<<16)
    DragAnObject_FunctionSVC = (1<<17)


class DraggableConstants(object):

    # .Bits
    Draggable_TypeDrag = 0
    Draggable_DragStartedAdjust = (1<<0)
    Draggable_TypeClickDrag = (1<<0)
    Draggable_TypeClickDoubleDrag = (1<<1)
    Draggable_DragStartedSelect = (1<<2)
    Draggable_DragStartedShift = (1<<3)
    Draggable_DragStartedCtrl = (1<<4)
    Action_DraggableDragStarted = 534663
    Action_DraggableDragEnded = 534664

    # .Int
    Draggable_TypeShift = 3

    # Gadget_Flags
    Draggable_GenerateDragStarted = (1<<0)
    Draggable_Sprite = (1<<1)
    Draggable_Text = (1<<2)
    Draggable_Type = 56
    Draggable_UseToolboxIds = (1<<6)
    Draggable_DropShadow = (1<<7)
    Draggable_NoDither = (1<<8)

    # Toolbox_Class
    Class_Draggable = 640


class FileinfoConstants(object):

    # .Bits
    Action_FileInfoAboutToBeShown = 535232
    Action_FileInfoDialogueCompleted = 535233
    Error_FileInfoTasksActive = 0x80b200
    Error_FileInfoAllocFailed = 0x80b201
    Error_FileInfoShortBuffer = 0x80b202
    Error_FileInfoNoSuchTask = 0x80b211
    Error_FileInfoNoSuchMethod = 0x80b212
    Error_FileInfoNoSuchMiscOpMethod = 0x80b213

    # FileInfo_Flags
    FileInfo_GenerateAboutToBeShown = (1<<0)
    FileInfo_GenerateDialogueCompleted = (1<<1)

    # Toolbox_C
    FileInfo_Date = 8563713
    FileInfo_FileSize = 8563714
    FileInfo_FileName = 8563715
    FileInfo_FileType = 8563716
    FileInfo_Modified = 8563717
    FileInfo_FileIcon = 8563718
    FileInfo_DateLabel = 8563719
    FileInfo_FileSizeLabel = 8563720
    FileInfo_ModifiedLabel = 8563721
    FileInfo_FileTypeLabel = 8563722

    # Toolbox_Class
    Class_FileInfo = 535232


class FontdboxConstants(object):

    # .Bits
    FontDbox_SetHeight = (1<<0)
    FontDbox_SetAspect = (1<<1)
    Action_FontDboxAboutToBeShown = 535040
    Action_FontDboxDialogueCompleted = 535041
    Action_FontDboxApplyFont = 535042
    Error_FontDboxTasksActive = 0x80af00
    Error_FontDboxAllocFailed = 0x80af01
    Error_FontDboxShortBuffer = 0x80af02
    Error_FontDboxNoSuchTask = 0x80af11
    Error_FontDboxNoSuchMethod = 0x80af12
    Error_FontDboxNoSuchMiscOpMethod = 0x80af13
    Error_FontDboxNoSuchFont = 0x80af14
    Error_FontDboxNoFonts = 0x80af21
    Error_FontDboxOutOfMessageSpace = 0x80af31

    # FontDbox_Flags
    FontDbox_GenerateAboutToBeShown = (1<<0)
    FontDbox_GenerateDialogueCompleted = (1<<1)
    FontDbox_IncludeSystemFont = (1<<2)

    # Toolbox_C
    FontDbox_Apply = 136970240
    FontDbox_Cancel = 136970241
    FontDbox_Try = 136970242
    FontDbox_TryString = 136970243
    FontDbox_AspectRatio = 136970244
    FontDbox_Height = 136970245
    FontDbox_StandardSize0 = 136970246
    FontDbox_StandardSize1 = 136970247
    FontDbox_StandardSize2 = 136970248
    FontDbox_StandardSize3 = 136970249
    FontDbox_StandardSize4 = 136970250
    FontDbox_StandardSize5 = 136970251
    FontDbox_StandardSize6 = 136970252
    FontDbox_StandardSize7 = 136970253
    FontDbox_StandardSize8 = 136970254
    FontDbox_StandardSize9 = 136970255
    FontDbox_Style = 136970256
    FontDbox_Weight = 136970257
    FontDbox_Font = 136970258

    # Toolbox_Class
    Class_FontDbox = 535040


class FontmenuConstants(object):

    # .Bits
    Action_FontMenuAboutToBeShown = 535104
    Action_FontMenuDialogueCompleted = 535105
    Action_FontMenuSelection = 535106
    Error_FontMenuTasksActive = 0x80b000
    Error_FontMenuAllocFailed = 0x80b001
    Error_FontMenuShortBuffer = 0x80b002
    Error_FontMenuNoSuchTask = 0x80b011
    Error_FontMenuNoSuchMethod = 0x80b012
    Error_FontMenuNoSuchMiscOpMethod = 0x80b013

    # FontMenu_Flags
    FontMenu_GenerateAboutToBeShown = (1<<0)
    FontMenu_GenerateDialogueCompleted = (1<<1)
    FontMenu_IncludeSystemFont = (1<<2)

    # Toolbox_Class
    Class_FontMenu = 535104


class FrontendConstants(object):
    pass


class GadgetConstants(object):

    # .Bits
    Gadget_NoHandler = 0
    Gadget_DefaultHandler = (1<<0)
    Gadget_PrivateHandler = (1<<1)

    # .Int
    Gadget_FeatureAddShift = 0
    Gadget_FeatureClickShift = 10
    Gadget_FeatureFadeShift = 22
    Gadget_FeatureMethodShift = 6
    Gadget_FeatureMoveShift = 20
    Gadget_FeaturePlotShift = 16
    Gadget_FeaturePostAddShift = 4
    Gadget_FeatureRemoveShift = 2
    Gadget_FeatureSetFocusShift = 18

    # Gadget_Feature
    Gadget_FeatureAdd = 3
    Gadget_FeatureRemove = 12
    Gadget_FeaturePostAdd = 48
    Gadget_FeatureMethod = 192
    Gadget_FeatureClick = 3072
    Gadget_FeaturePlot = 196608
    Gadget_FeatureSetFocus = 786432
    Gadget_FeatureMove = 3145728
    Gadget_FeatureFade = 12582912

    # Gadget_Flags
    Gadget_AtBack = (1<<30)
    Gadget_Faded = (1<<31)


class IconbarConstants(object):

    # .Bits
    Iconbar_ClickedAdjust = (1<<0)
    Iconbar_ClickedSelect = (1<<2)
    Action_IconbarClicked = 534784
    Action_IconbarSelectAboutToBeShown = 534785
    Action_IconbarAdjustAboutToBeShown = 534786
    Error_IconbarAllocFailed = 0x80ab01
    Error_IconbarShortBuffer = 0x80ab02
    Error_IconbarBadObjectVersion = 0x80ab03
    Error_IconbarBadFlags = 0x80ab04
    Error_IconbarNoSuchTask = 0x80ab11
    Error_IconbarNoSuchMethod = 0x80ab12
    Error_IconbarNoSuchMiscOpMethod = 0x80ab13
    Error_IconbarWrongShowType = 0x80ab14
    Error_IconbarNoText = 0x80ab20
    Error_IconbarTasksActive = 0x80ab21

    # Iconbar_Flags
    Iconbar_GenerateSelectAboutToBeShown = (1<<0)
    Iconbar_GenerateAdjustAboutToBeShown = (1<<1)
    Iconbar_SelectIsMenu = (1<<2)
    Iconbar_AdjustIsMenu = (1<<3)
    Iconbar_GenerateSelectClicked = (1<<5)
    Iconbar_GenerateAdjustClicked = (1<<6)
    Iconbar_HasText = (1<<4)

    # Iconbar_SetButton
    Iconbar_Select = 1
    Iconbar_Adjust = 2

    # Toolbox_Class
    Class_Iconbar = 534784


class KeyboardshortcutConstants(object):

    # KeyboardShortcut_Flags
    KeyboardShortcut_ShowAsMenu = (1<<0)


class LabelConstants(object):

    # .Bits
    Label_NoBox = (1<<0)
    Label_RJustified = (1<<1)
    Label_HCentred = (1<<2)

    # Toolbox_Class
    Class_Label = 320


class LabelledboxConstants(object):

    # Gadget_Flags
    LabelledBox_Sprite = (1<<0)
    LabelledBox_SpriteIsFilled = (1<<1)

    # Toolbox_Class
    Class_LabelledBox = 256


class MenuConstants(object):

    # .Bits
    Action_MenuAboutToBeShown = 534720
    Action_MenuDialogueCompleted = 534721
    Action_MenuSubMenu = 534722
    Action_MenuSelection = 534723
    Error_MenuTasksActive = 0x80aa00
    Error_MenuAllocFailed = 0x80aa01
    Error_MenuShortBuffer = 0x80aa02
    Error_MenuNoSuchTask = 0x80aa11
    Error_MenuNoSuchMethod = 0x80aa12
    Error_MenuNoSuchMiscOpMethod = 0x80aa13
    Error_MenuNoSuchComponent = 0x80aa14
    Error_MenuSpriteNotText = 0x80aa21
    Error_MenuTextNotSprite = 0x80aa22
    Error_MenuNoTopMenu = 0x80aa31
    Error_MenuUnknownSubMenu = 0x80aa32
    Error_MenuNoSpriteName = 0x80aa33

    # Menu_AddAt
    Menu_AddAtEnd = -2
    Menu_AddAtStart = -1

    # Menu_AddFlags
    Menu_AddBefore = (1<<0)

    # Menu_EntryFlags
    Menu_EntryTicked = (1<<0)
    Menu_EntrySeparate = (1<<1)
    Menu_EntryFaded = (1<<8)
    Menu_EntryIsSprite = (1<<9)
    Menu_EntrySubMenu = (1<<10)
    Menu_EntryGenerateSubMenuAction = (1<<11)
    Menu_EntryIsMenu = (1<<12)

    # Menu_Flags
    Menu_GenerateAboutToBeShown = (1<<0)
    Menu_GenerateDialogueCompleted = (1<<1)

    # Menu_ShowFlags
    Menu_ShowPersistent = 0
    Menu_ShowTransient = (1<<0)

    # Toolbox_Class
    Class_Menu = 534720


class NumberrangeConstants(object):

    # .Bits
    NumberRange_GetNumericalField = (1<<0)
    NumberRange_GetLeftAdjuster = (1<<1)
    NumberRange_GetRightAdjuster = (1<<2)
    NumberRange_GetSlider = (1<<3)
    Action_NumberRangeValueChanged = 534669

    # .Int
    NumberRange_ColourShift = 8
    NumberRange_SliderTypeLeft = 2
    NumberRange_SliderTypeNone = 0
    NumberRange_SliderTypeRight = 1
    NumberRange_SliderTypeShift = 5

    # Gadget_Flags
    NumberRange_GenerateValueChanged = (1<<0)
    NumberRange_GenerateSetValueChanged = (1<<1)
    NumberRange_Writable = (1<<2)
    NumberRange_HasNumericalDisplay = (1<<3)
    NumberRange_Adjusters = (1<<4)
    NumberRange_SliderType = 224
    NumberRange_Colour = 3840

    # NumberRange_BoundsFlags
    NumberRange_BoundLower = (1<<0)
    NumberRange_BoundUpper = (1<<1)
    NumberRange_BoundStep = (1<<2)
    NumberRange_BoundPrecision = (1<<3)

    # Toolbox_Class
    Class_NumberRange = 832


class OptionbuttonConstants(object):

    # .Bits
    OptionButton_StateChangedAdjust = (1<<0)
    OptionButton_StateChangedSelect = (1<<2)
    Action_OptionButtonStateChanged = 534658

    # Toolbox_Class
    Class_OptionButton = 192


class PopupConstants(object):

    # .Bits
    Action_PopUpAboutToBeShown = 534667

    # Gadget_Flags
    PopUp_GenerateAboutToBeShown = (1<<0)

    # Toolbox_Class
    PopUp_Class = 704


class PrintdboxConstants(object):

    # .Bits
    PrintDbox_PrintSideways = (1<<0)
    PrintDbox_PrintDraft = (1<<1)
    Action_PrintDboxAboutToBeShown = 535296
    Action_PrintDboxDialogueCompleted = 535297
    Action_PrintDboxSetUpAboutToBeShown = 535298
    Action_PrintDboxSave = 535299
    Action_PrintDboxSetUp = 535300
    Action_PrintDboxPrint = 535301
    Error_PrintDboxTasksActive = 0x80b300
    Error_PrintDboxAllocFailed = 0x80b301
    Error_PrintDboxShortBuffer = 0x80b302
    Error_PrintDboxNoSuchTask = 0x80b311
    Error_PrintDboxNoSuchMethod = 0x80b312
    Error_PrintDboxNoSuchMiscOpMethod = 0x80b313

    # .Int
    PrintDbox_PageRangeAll = -1

    # PrintDbox_Flags
    PrintDbox_GenerateAboutToBeShown = (1<<0)
    PrintDbox_GenerateDialogueCompleted = (1<<1)
    PrintDbox_GenerateShowSetupAction = (1<<2)
    PrintDbox_IncludeAllFromTo = (1<<3)
    PrintDbox_IncludeCopies = (1<<4)
    PrintDbox_IncludeScale = (1<<5)
    PrintDbox_IncludeOrientation = (1<<6)
    PrintDbox_IncludeSave = (1<<7)
    PrintDbox_IncludeSetUp = (1<<8)
    PrintDbox_IncludeDraft = (1<<9)
    PrintDbox_SelectFromTo = (1<<10)
    PrintDbox_SelectSideways = (1<<11)
    PrintDbox_SelectDraft = (1<<12)

    # Toolbox_C
    PrintDbox_Print = 137035776
    PrintDbox_Save = 137035777
    PrintDbox_Cancel = 137035778
    PrintDbox_FromTo = 137035779
    PrintDbox_All = 137035780
    PrintDbox_From = 137035781
    PrintDbox_Upright = 137035785
    PrintDbox_Sideways = 137035786
    PrintDbox_Draft = 137035787
    PrintDbox_SetUp = 137035788
    PrintDbox_To = 137035789
    PrintDbox_Copies = 137035790
    PrintDbox_Scale = 137035791
    PrintDbox_Percent = 137035792


class ProginfoConstants(object):

    # .Bits
    Action_ProgInfoAboutToBeShown = 535360
    Action_ProgInfoDialogueCompleted = 535361
    Error_ProgInfoTasksActive = 0x80b400
    Error_ProgInfoAllocFailed = 0x80b401
    Error_ProgInfoShortBuffer = 0x80b402
    Error_ProgInfoNoSuchTask = 0x80b411
    Error_ProgInfoNoSuchMethod = 0x80b412
    Error_ProgInfoNoSuchMiscOpMethod = 0x80b413

    # .Int
    ProgInfo_LicenceAuthority = 5
    ProgInfo_LicenceNetwork = 4
    ProgInfo_LicencePublicDomain = 0
    ProgInfo_LicenceSingleMachine = 2
    ProgInfo_LicenceSingleUser = 1
    ProgInfo_LicenceSite = 3

    # ProgInfo_Flags
    ProgInfo_GenerateAboutToBeShown = (1<<0)
    ProgInfo_GenerateDialogueCompleted = (1<<1)
    ProgInfo_IncludeLicenceType = (1<<2)

    # Toolbox_C
    ProgInfo_Name = 8565760
    ProgInfo_Purpose = 8565761
    ProgInfo_Author = 8565762
    ProgInfo_LicenceType = 8565763
    ProgInfo_Version = 8565764
    ProgInfo_NameLabel = 8565765
    ProgInfo_PurposeLabel = 8565766
    ProgInfo_AuthorLabel = 8565767
    ProgInfo_LicenceLabel = 8565768
    ProgInfo_VersionLabel = 8565769

    # Toolbox_Class
    Class_ProgInfo = 535360


class QuitConstants(object):

    # .Bits
    Action_QuitAboutToBeShown = 535184
    Action_QuitQuit = 535185
    Action_QuitDialogueCompleted = 535186
    Action_QuitCancel = 535187

    # Quit_Flags
    Quit_GenerateAboutToBeShown = (1<<0)
    Quit_GenerateDialogueCompleted = (1<<1)

    # Toolbox_C
    Quit_FileTypeIcon = 8562944
    Quit_Quit = 8562945
    Quit_Cancel = 8562946

    # Toolbox_Class
    Class_Quit = 535184


class RadiobuttonConstants(object):

    # .Bits
    RadioButton_StateChangedAdjust = (1<<0)
    RadioButton_StateChangedSelect = (1<<2)
    Action_RadioButtonStateChanged = 534659

    # Gadget_Flags
    RadioButton_GenerateStateChanged = (1<<0)
    RadioButton_GenerateSetStateChanged = (1<<1)
    RadioButton_On = (1<<2)

    # Toolbox_Class
    Class_RadioButton = 384


class SaveasConstants(object):

    # .Bits
    Action_SaveAsAboutToBeShown = 535488
    Action_SaveAsDialogueCompleted = 535489
    Action_SaveAsSaveToFile = 535490
    Action_SaveAsFillBuffer = 535491
    Action_SaveAsSaveCompleted = 535492
    Error_SaveAsTasksActive = 0x80b600
    Error_SaveAsAllocFailed = 0x80b601
    Error_SaveAsShortBuffer = 0x80b602
    Error_SaveAsFileNameTooLong = 0x80b603
    Error_SaveAsNoSuchTask = 0x80b611
    Error_SaveAsNoSuchMethod = 0x80b612
    Error_SaveAsNoSuchMiscOpMethod = 0x80b613
    Error_SaveAsNotType1 = 0x80b621
    Error_SaveAsNotType3 = 0x80b623
    Error_SaveAsBufferExceeded = 0x80b631
    Error_SaveAsDataAddressUnset = 0x80b641
    Error_SaveAsNotFullPath = 0x80b642

    # .Int
    SaveAs_SaveSafe = 2
    SaveAs_SaveSelection = 1

    # SaveAs_Flags
    SaveAs_GenerateAboutToBeShown = (1<<0)
    SaveAs_GenerateDialogueCompleted = (1<<1)
    SaveAs_NoSelectionButton = (1<<2)
    SaveAs_GivenData = (1<<3)
    SaveAs_ClientSupportsRAMTransfer = (1<<4)

    # Toolbox_C
    SaveAs_FileIcon = 137084928
    SaveAs_FileName = 137084929
    SaveAs_Cancel = 137084930
    SaveAs_Save = 137084931
    SaveAs_Selection = 137084932

    # Toolbox_Class
    Class_SaveAs = 535488


class ScaleConstants(object):

    # .Bits
    Scale_SetLowerBound = (1<<0)
    Scale_SetUpperBound = (1<<1)
    Scale_SetStepSize = (1<<2)
    Action_ScaleAboutToBeShown = 535552
    Action_ScaleDialogueCompleted = 535553
    Action_ScaleApplyFactor = 535554
    Error_ScaleTasksActive = 0x80b700
    Error_ScaleAllocFailed = 0x80b701
    Error_ScaleShortBuffer = 0x80b702
    Error_ScaleNoSuchTask = 0x80b711
    Error_ScaleNoSuchMethod = 0x80b712
    Error_ScaleNoSuchMiscOpMethod = 0x80b713

    # Scale_Flags
    Scale_GenerateAboutToBeShown = (1<<0)
    Scale_GenerateDialogueCompleted = (1<<1)
    Scale_IncludeScaleToFit = (1<<2)

    # Toolbox_C
    Scale_Percent = 8568832
    Scale_StdValue0 = 8568833
    Scale_StdValue1 = 8568834
    Scale_StdValue2 = 8568835
    Scale_StdValue3 = 8568836
    Scale_Cancel = 8568837
    Scale_Scale = 8568838
    Scale_PercentLabel = 8568839
    Scale_ScaleLabel = 8568840
    Scale_ScaleToFit = 8568841

    # Toolbox_Class
    Class_Scale = 535552


class SliderConstants(object):

    # .Bits
    Slider_ValueChanging = (1<<0)
    Slider_ValueChangedByDragging = (1<<1)
    Slider_ValueChanged = (1<<2)
    Action_SliderValueChanged = 534662

    # .Int
    Slider_KnobColourShift = 12
    Slider_WellColourShift = 16

    # Gadget_Flags
    Slider_GenerateValueChanged = (1<<0)
    Slider_GenerateValueChangedByDragging = (1<<1)
    Slider_GenerateSetValueChanged = (1<<2)
    Slider_Vertical = (1<<3)
    Slider_Draggable = (1<<4)
    Slider_KnobColour = 61440
    Slider_WellColour = 983040

    # Slider_BoundsFlags
    Slider_BoundLower = (1<<0)
    Slider_BoundUpper = (1<<1)
    Slider_BoundStep = (1<<2)

    # Toolbox_Class
    Class_Slider = 576


class StringsetConstants(object):

    # .Bits
    StringSet_JustificationLeft = 0
    StringSet_ValueTooLong = (1<<0)
    StringSet_JustificationRight = (1<<0)
    StringSet_GetAlphanumericField = (1<<0)
    StringSet_GetPopUpMenu = (1<<1)
    StringSet_JustificationCentred = (1<<1)
    Action_StringSetValueChanged = 534670
    Action_StringSetAboutToBeShown = 534671

    # .Int
    StringSet_JustificationShift = 5

    # Gadget_Flags
    StringSet_GenerateUserValueChanged = (1<<0)
    StringSet_GenerateSetValueChanged = (1<<1)
    StringSet_Writable = (1<<2)
    StringSet_GenerateAboutToBeShown = (1<<3)
    StringSet_NoDisplay = (1<<4)
    StringSet_Justification = 96

    # Toolbox_Class
    StringSet_Class = 896


class ToolboxConstants(object):

    # .Bits
    Action_Error = 282304
    Action_ObjectAutoCreated = 282305
    Action_ObjectDeleted = 282306
    Error_ToolboxNoMem = 0x80cb00
    Error_ToolboxBadSWI = 0x80cb01
    Error_ToolboxInvalidObjectID = 0x80cb02
    Error_ToolboxNotAToolboxTask = 0x80cb03
    Error_ToolboxNoDirName = 0x80cb04
    Error_ToolboxNoMsgsFD = 0x80cb05
    Error_ToolboxNoIDBlock = 0x80cb06
    Error_ToolboxBadResFile = 0x80cb07
    Error_ToolboxTasksActive = 0x80cb08
    Error_ToolboxTemplateNotFound = 0x80cb09
    Error_ToolboxNoSuchPreFilter = 0x80cb0a
    Error_ToolboxNotAResFile = 0x80cb0b
    Error_ToolboxBadResFileVersion = 0x80cb0c
    Error_ToolboxBadFlags = 0x80cb0d
    Toolbox_Event = (1<<9)

    # .Int
    Toolbox_NameLimit = 12
    Toolbox_RelocateMsgReference = 2
    Toolbox_RelocateObjectOffset = 4
    Toolbox_RelocateSpriteAreaReference = 3
    Toolbox_RelocateStringReference = 1
    Toolbox_ResourceFileVersion = 101

    # Toolbox_C
    Toolbox_NullComponent = -1

    # Toolbox_Class
    Toolbox_All = -1
    Toolbox_AnyPostFilter = -1
    Toolbox_WimpObjectPostFilter = 0
    Toolbox_WimpObjects = 0

    # Toolbox_CreateFlags
    Toolbox_CreateGivenObject = (1<<0)

    # Toolbox_DeleteFlags
    Toolbox_DeleteNoRecurse = (1<<0)

    # Toolbox_FilterType
    Toolbox_RegisterEventFilter = 1
    Toolbox_RegisterMessageFilter = 2
    Toolbox_RegisterActionFilter = 3

    # Toolbox_Info
    Toolbox_InfoShowing = 1

    # Toolbox_O
    Toolbox_NullObject = 0

    # Toolbox_ObjectFlags
    Toolbox_ObjectCreateOnLoad = (1<<0)
    Toolbox_ObjectShowOnCreate = (1<<1)
    Toolbox_ObjectShared = (1<<2)
    Toolbox_ObjectAncestor = (1<<3)

    # Toolbox_PositionTag
    Toolbox_PositionDefault = 0
    Toolbox_PositionFull = 1
    Toolbox_PositionTopLeft = 2

    # Toolbox_RegisterFlags
    Toolbox_DeRegisterFilter = (1<<0)

    # Toolbox_ShowFlags
    Toolbox_ShowAsMenu = (1<<0)
    Toolbox_ShowAsSubMenu = (1<<1)


class WindowConstants(object):

    # .Bits
    Action_WindowAboutToBeShown = 534656
    Action_WindowDialogueCompleted = 534672
    Error_WindowAllocFailed = 0x80a901
    Error_WindowShortBuffer = 0x80a902
    Error_WindowBadVersion = 0x80a903
    Error_WindowInvalidFlags = 0x80a904
    Error_WindowTasksActive = 0x80a905
    Error_WindowNoSuchTask = 0x80a911
    Error_WindowNoSuchMethod = 0x80a912
    Error_WindowNoSuchMiscOpMethod = 0x80a913
    Error_WindowInvalidComponentID = 0x80a914
    Error_WindowDuplicateComponentID = 0x80a915
    Error_WindowInvalidGadgetType = 0x80a920

    # .Int
    Window_NoFocus = -1
    Window_SetFocusToWindow = -2

    # Toolbox_Class
    Class_Window = 534656

    # Window_Flags
    Window_GenerateAboutToBeShown = (1<<0)
    Window_AutoOpen = (1<<1)
    Window_AutoClose = (1<<2)
    Window_GenerateDialogueCompleted = (1<<3)
    Window_IsToolBar = (1<<4)

    # Window_MouseState
    Window_ClickAdjust = 1
    Window_ClickMenu = 2
    Window_ClickSelect = 4
    Window_ClickNotToolbox = 256

    # Window_ToolBarFlags
    Window_ToolBarIBL = (1<<0)
    Window_ToolBarITL = (1<<1)
    Window_ToolBarEBL = (1<<2)
    Window_ToolBarETL = (1<<3)


class WindowsupportexternalConstants(object):

    # .Int
    WindowSupportExternal_HandlerAdd = 1
    WindowSupportExternal_HandlerClick = 6
    WindowSupportExternal_HandlerFade = 3
    WindowSupportExternal_HandlerMethod = 4
    WindowSupportExternal_HandlerMove = 11
    WindowSupportExternal_HandlerPlot = 9
    WindowSupportExternal_HandlerPostAdd = 12
    WindowSupportExternal_HandlerRemove = 2
    WindowSupportExternal_HandlerSetFocus = 10


class WritablefieldConstants(object):

    # .Bits
    WritableField_GenerateUserValueChanged = (1<<0)
    WritableField_ValueTooLong = (1<<0)
    WritableField_GenerateSetValueChanged = (1<<1)
    WritableField_RJustified = (1<<2)
    WritableField_HCentred = (1<<3)
    WritableField_ConcealText = (1<<4)
    Action_WritableFieldValueChanged = 534661

    # Toolbox_Class
    Class_WritableField = 512
