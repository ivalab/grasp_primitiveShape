function [vrep] = remApiSetup()
    % Scene object types
    vrep.sim_object_shape_type           =0;
    vrep.sim_object_joint_type           =1;
    vrep.sim_object_graph_type           =2;
    vrep.sim_object_camera_type          =3;
    vrep.sim_object_dummy_type           =4;
    vrep.sim_object_proximitysensor_type =5;
    vrep.sim_object_reserved1            =6;
    vrep.sim_object_reserved2            =7;
    vrep.sim_object_path_type            =8;
    vrep.sim_object_visionsensor_type    =9;
    vrep.sim_object_volume_type          =10;
    vrep.sim_object_mill_type            =11;
    vrep.sim_object_forcesensor_type     =12;
    vrep.sim_object_light_type           =13;
    vrep.sim_object_mirror_type          =14;

    %General object types
    vrep.sim_appobj_object_type          =109;
    vrep.sim_appobj_collision_type       =110;
    vrep.sim_appobj_distance_type        =111;
    vrep.sim_appobj_simulation_type      =112;
    vrep.sim_appobj_ik_type              =113;
    vrep.sim_appobj_constraintsolver_type=114;
    vrep.sim_appobj_collection_type      =115;
    vrep.sim_appobj_ui_type              =116;
    vrep.sim_appobj_script_type          =117;
    vrep.sim_appobj_pathplanning_type    =118;
    vrep.sim_appobj_RESERVED_type        =119;
    vrep.sim_appobj_texture_type         =120;

    % Ik calculation methods
    vrep.sim_ik_pseudo_inverse_method        =0;
    vrep.sim_ik_damped_least_squares_method  =1;
    vrep.sim_ik_jacobian_transpose_method    =2;

    % Ik constraints
    vrep.sim_ik_x_constraint         =1;
    vrep.sim_ik_y_constraint         =2;
    vrep.sim_ik_z_constraint         =4;
    vrep.sim_ik_alpha_beta_constraint=8;
    vrep.sim_ik_gamma_constraint     =16;
    vrep.sim_ik_avoidance_constraint =64;

    % Ik calculation results
    vrep.sim_ikresult_not_performed  =0;
    vrep.sim_ikresult_success        =1;
    vrep.sim_ikresult_fail           =2;

    % Scene object sub-types
    vrep.sim_light_omnidirectional_subtype   =1;
    vrep.sim_light_spot_subtype              =2;
    vrep.sim_light_directional_subtype       =3;
    vrep.sim_joint_revolute_subtype          =10;
    vrep.sim_joint_prismatic_subtype         =11;
    vrep.sim_joint_spherical_subtype         =12;
    vrep.sim_shape_simpleshape_subtype       =20;
    vrep.sim_shape_multishape_subtype        =21;
    vrep.sim_proximitysensor_pyramid_subtype =30;
    vrep.sim_proximitysensor_cylinder_subtype=31;
    vrep.sim_proximitysensor_disc_subtype    =32;
    vrep.sim_proximitysensor_cone_subtype    =33;
    vrep.sim_proximitysensor_ray_subtype     =34;
    vrep.sim_mill_pyramid_subtype            =40;
    vrep.sim_mill_cylinder_subtype           =41;
    vrep.sim_mill_disc_subtype               =42;
    vrep.sim_mill_cone_subtype               =42;
    vrep.sim_object_no_subtype               =200;

    %Scene object main properties
    vrep.sim_objectspecialproperty_collidable                       =1;
    vrep.sim_objectspecialproperty_measurable                   =2;
    vrep.sim_objectspecialproperty_detectable_ultrasonic            =16;
    vrep.sim_objectspecialproperty_detectable_infrared          =32;
    vrep.sim_objectspecialproperty_detectable_laser             =64;
    vrep.sim_objectspecialproperty_detectable_inductive         =128;
    vrep.sim_objectspecialproperty_detectable_capacitive            =256;
    vrep.sim_objectspecialproperty_renderable                   =512;
    vrep.sim_objectspecialproperty_detectable_all               =496;
    vrep.sim_objectspecialproperty_cuttable                     =1024;
    vrep.sim_objectspecialproperty_pathplanning_ignored         =2048;

    % Model properties
    vrep.sim_modelproperty_not_collidable               =1;
    vrep.sim_modelproperty_not_measurable               =2;
    vrep.sim_modelproperty_not_renderable               =4;
    vrep.sim_modelproperty_not_detectable               =8;
    vrep.sim_modelproperty_not_cuttable                 =16;
    vrep.sim_modelproperty_not_dynamic                  =32;
    vrep.sim_modelproperty_not_respondable              =64;
    vrep.sim_modelproperty_not_reset                        =128;
    vrep.sim_modelproperty_not_visible                  =256;
    vrep.sim_modelproperty_not_model                        =61440;

    % Check the documentation instead of comments below!!
    vrep.sim_message_ui_button_state_change  =0;
    vrep.sim_message_reserved9               =1;
    vrep.sim_message_object_selection_changed=2;
    vrep.sim_message_reserved10             =3;
    vrep.sim_message_model_loaded            =4;
    vrep.sim_message_reserved11             =5;
    vrep.sim_message_keypress               =6;
    vrep.sim_message_bannerclicked          =7;
    vrep.sim_message_for_c_api_only_start        =256;
    vrep.sim_message_reserved1                   =257;
    vrep.sim_message_reserved2                  =258;
    vrep.sim_message_reserved3                  =259;
    vrep.sim_message_eventcallback_scenesave        =260;
    vrep.sim_message_eventcallback_modelsave        =261;
    vrep.sim_message_eventcallback_moduleopen   =262;
    vrep.sim_message_eventcallback_modulehandle =263;
    vrep.sim_message_eventcallback_moduleclose  =264;
    vrep.sim_message_reserved4                  =265;
    vrep.sim_message_reserved5                  =266;
    vrep.sim_message_reserved6                  =267;
    vrep.sim_message_reserved7                  =268;
    vrep.sim_message_eventcallback_instancepass =269;
    vrep.sim_message_eventcallback_broadcast     =270;
    vrep.sim_message_eventcallback_imagefilter_enumreset =271;
    vrep.sim_message_eventcallback_imagefilter_enumerate      =272;
    vrep.sim_message_eventcallback_imagefilter_adjustparams   =273;
    vrep.sim_message_eventcallback_imagefilter_reserved       =274;
    vrep.sim_message_eventcallback_imagefilter_process        =275;
    vrep.sim_message_eventcallback_reserved1                  =276;
    vrep.sim_message_eventcallback_reserved2                  =277;
    vrep.sim_message_eventcallback_reserved3                  =278;
    vrep.sim_message_eventcallback_reserved4                  =279;
    vrep.sim_message_eventcallback_abouttoundo               =280;
    vrep.sim_message_eventcallback_undoperformed                 =281;
    vrep.sim_message_eventcallback_abouttoredo               =282;
    vrep.sim_message_eventcallback_redoperformed                 =283;
    vrep.sim_message_eventcallback_scripticondblclick         =284;
    vrep.sim_message_eventcallback_simulationabouttostart     =285;
    vrep.sim_message_eventcallback_simulationended            =286;
    vrep.sim_message_eventcallback_reserved5                     =287;
    vrep.sim_message_eventcallback_keypress                  =288;
    vrep.sim_message_eventcallback_modulehandleinsensingpart  =289;
    vrep.sim_message_eventcallback_renderingpass              =290;
    vrep.sim_message_eventcallback_bannerclicked              =291;
    vrep.sim_message_eventcallback_menuitemselected           =292;
    vrep.sim_message_eventcallback_refreshdialogs             =293;
    vrep.sim_message_eventcallback_sceneloaded                =294;
    vrep.sim_message_eventcallback_modelloaded                =295;
    vrep.sim_message_eventcallback_instanceswitch             =296;
    vrep.sim_message_eventcallback_guipass                    =297;
    vrep.sim_message_eventcallback_mainscriptabouttobecalled  =298;
    vrep.sim_message_eventcallback_rmlposition                =299;
    vrep.sim_message_eventcallback_rmlvelocity                =300;

    vrep.sim_message_simulation_start_resume_request          =4096;
    vrep.sim_message_simulation_pause_request                 =4097;
    vrep.sim_message_simulation_stop_request                  =4098;

    % Scene object properties
    vrep.sim_objectproperty_collapsed               =16;
    vrep.sim_objectproperty_selectable              =32;
    vrep.sim_objectproperty_reserved7               =64;
    vrep.sim_objectproperty_selectmodelbaseinstead  =128;
    vrep.sim_objectproperty_dontshowasinsidemodel   =256;

    % type of arguments (input and output) for custom lua commands
    vrep.sim_lua_arg_nil     =0;
    vrep.sim_lua_arg_bool   =1;
    vrep.sim_lua_arg_int     =2;
    vrep.sim_lua_arg_float   =3;
    vrep.sim_lua_arg_string  =4;
    vrep.sim_lua_arg_invalid =5;
    vrep.sim_lua_arg_table   =8;

    % custom user interface properties
    vrep.sim_ui_property_visible                        =1;
    vrep.sim_ui_property_visibleduringsimulationonly    =2;
    vrep.sim_ui_property_moveable                   =4;
    vrep.sim_ui_property_relativetoleftborder       =8;
    vrep.sim_ui_property_relativetotopborder            =16;
    vrep.sim_ui_property_fixedwidthfont             =32;
    vrep.sim_ui_property_systemblock                    =64;
    vrep.sim_ui_property_settocenter                    =128;
    vrep.sim_ui_property_rolledup                   =256;
    vrep.sim_ui_property_selectassociatedobject     =512;
    vrep.sim_ui_property_visiblewhenobjectselected  =1024;

    % button properties
    vrep.sim_buttonproperty_button              =0;
    vrep.sim_buttonproperty_label               =1;
    vrep.sim_buttonproperty_slider              =2;
    vrep.sim_buttonproperty_editbox             =3;
    vrep.sim_buttonproperty_staydown                =8;
    vrep.sim_buttonproperty_enabled             =16;
    vrep.sim_buttonproperty_borderless          =32;
    vrep.sim_buttonproperty_horizontallycentered    =64;
    vrep.sim_buttonproperty_ignoremouse         =128;
    vrep.sim_buttonproperty_isdown              =256;
    vrep.sim_buttonproperty_transparent         =512;
    vrep.sim_buttonproperty_nobackgroundcolor   =1024;
    vrep.sim_buttonproperty_rollupaction            =2048;
    vrep.sim_buttonproperty_closeaction         =4096;
    vrep.sim_buttonproperty_verticallycentered  =8192;
    vrep.sim_buttonproperty_downupevent         =16384;

    % Simulation status
    vrep.sim_simulation_stopped                     =0;
    vrep.sim_simulation_paused                      =8;
    vrep.sim_simulation_advancing                   =16;
    vrep.sim_simulation_advancing_firstafterstop        =16;
    vrep.sim_simulation_advancing_running           =17;
    vrep.sim_simulation_advancing_lastbeforepause   =19;
    vrep.sim_simulation_advancing_firstafterpause   =20;
    vrep.sim_simulation_advancing_abouttostop       =21;
    vrep.sim_simulation_advancing_lastbeforestop        =22;

    % Script execution result (first return value)
    vrep.sim_script_no_error                    =0;
    vrep.sim_script_main_script_nonexistent =1;
    vrep.sim_script_main_script_not_called  =2;
    vrep.sim_script_reentrance_error            =4;
    vrep.sim_script_lua_error               =8;
    vrep.sim_script_call_error              =16;

    % Script types
    vrep.sim_scripttype_mainscript   =0;
    vrep.sim_scripttype_childscript  =1;
    vrep.sim_scripttype_jointctrlcallback  =4;
    vrep.sim_scripttype_contactcallback  =5;
    vrep.sim_scripttype_customizationscript  =6;
    vrep.sim_scripttype_generalcallback  =7;

    % API call error messages
    vrep.sim_api_errormessage_ignore    =0;
    vrep.sim_api_errormessage_report    =1;
    vrep.sim_api_errormessage_output    =2;

    % special argument of some functions
    vrep.sim_handle_all                     =-2;
    vrep.sim_handle_all_except_explicit     =-3;
    vrep.sim_handle_self                        =-4;
    vrep.sim_handle_main_script             =-5;
    vrep.sim_handle_tree                        =-6;
    vrep.sim_handle_chain                   =-7;
    vrep.sim_handle_single                  =-8;
    vrep.sim_handle_default                 =-9;
    vrep.sim_handle_all_except_self         =-10;
    vrep.sim_handle_parent                  =-11;

    % special handle flags
    vrep.sim_handleflag_assembly                =4194304;
    vrep.sim_handleflag_model               =8388608;

    % distance calculation methods
    vrep.sim_distcalcmethod_dl               =0;
    vrep.sim_distcalcmethod_dac              =1;
    vrep.sim_distcalcmethod_max_dl_dac       =2;
    vrep.sim_distcalcmethod_dl_and_dac       =3;
    vrep.sim_distcalcmethod_sqrt_dl2_and_dac2=4;
    vrep.sim_distcalcmethod_dl_if_nonzero    =5;
    vrep.sim_distcalcmethod_dac_if_nonzero   =6;

    % Generic dialog styles
    vrep.sim_dlgstyle_message       =0;
    vrep.sim_dlgstyle_input          =1;
    vrep.sim_dlgstyle_ok             =2;
    vrep.sim_dlgstyle_ok_cancel      =3;
    vrep.sim_dlgstyle_yes_no         =4;
    vrep.sim_dlgstyle_dont_center   =32;

    % Generic dialog return values
    vrep.sim_dlgret_still_open   =0;
    vrep.sim_dlgret_ok           =1;
    vrep.sim_dlgret_cancel       =2;
    vrep.sim_dlgret_yes          =3;
    vrep.sim_dlgret_no           =4;

    % Path properties
    vrep.sim_pathproperty_show_line                         =1;
    vrep.sim_pathproperty_show_orientation                  =2;
    vrep.sim_pathproperty_closed_path                       =4;
    vrep.sim_pathproperty_automatic_orientation             =8;
    vrep.sim_pathproperty_invert_velocity                   =16;
    vrep.sim_pathproperty_infinite_acceleration             =32;
    vrep.sim_pathproperty_flat_path                         =64;
    vrep.sim_pathproperty_show_position                     =128;
    vrep.sim_pathproperty_auto_velocity_profile_translation =256;
    vrep.sim_pathproperty_auto_velocity_profile_rotation        =512;
    vrep.sim_pathproperty_endpoints_at_zero                 =1024;
    vrep.sim_pathproperty_keep_x_up                         =2048;

    % drawing objects
    vrep.sim_drawing_points          =0;
    vrep.sim_drawing_lines          =1;
    vrep.sim_drawing_triangles      =2;
    vrep.sim_drawing_trianglepoints =3;
    vrep.sim_drawing_quadpoints     =4;
    vrep.sim_drawing_discpoints     =5;
    vrep.sim_drawing_cubepoints     =6;
    vrep.sim_drawing_spherepoints   =7;

    vrep.sim_drawing_itemcolors             =32;
    vrep.sim_drawing_vertexcolors           =64;
    vrep.sim_drawing_itemsizes              =128;
    vrep.sim_drawing_backfaceculling            =256;
    vrep.sim_drawing_wireframe              =512;
    vrep.sim_drawing_painttag               =1024;
    vrep.sim_drawing_followparentvisibility =2048;
    vrep.sim_drawing_cyclic                 =4096;
    vrep.sim_drawing_50percenttransparency  =8192;
    vrep.sim_drawing_25percenttransparency  =16384;
    vrep.sim_drawing_12percenttransparency  =32768;
    vrep.sim_drawing_emissioncolor          =65536;
    vrep.sim_drawing_facingcamera           =131072;
    vrep.sim_drawing_overlay                    =262144;
    vrep.sim_drawing_itemtransparency       =524288;

    % banner values
    vrep.sim_banner_left                        =1;
    vrep.sim_banner_right                   =2;
    vrep.sim_banner_nobackground                =4;
    vrep.sim_banner_overlay                 =8;
    vrep.sim_banner_followparentvisibility  =16;
    vrep.sim_banner_clickselectsparent      =32;
    vrep.sim_banner_clicktriggersevent      =64;
    vrep.sim_banner_facingcamera                =128;
    vrep.sim_banner_fullyfacingcamera       =256;
    vrep.sim_banner_backfaceculling         =512;
    vrep.sim_banner_keepsamesize                =1024;
    vrep.sim_banner_bitmapfont              =2048;

    % particle objects
    vrep.sim_particle_points1        =0;
    vrep.sim_particle_points2       =1;
    vrep.sim_particle_points4       =2;
    vrep.sim_particle_roughspheres  =3;
    vrep.sim_particle_spheres       =4;

    vrep.sim_particle_respondable1to4       =32;
    vrep.sim_particle_respondable5to8       =64;
    vrep.sim_particle_particlerespondable   =128;
    vrep.sim_particle_ignoresgravity            =256;
    vrep.sim_particle_invisible             =512;
    vrep.sim_particle_itemsizes             =1024;
    vrep.sim_particle_itemdensities         =2048;
    vrep.sim_particle_itemcolors                =4096;
    vrep.sim_particle_cyclic                    =8192;
    vrep.sim_particle_emissioncolor         =16384;
    vrep.sim_particle_water                 =32768;
    vrep.sim_particle_painttag              =65536;

    % custom user interface menu attributes
    vrep.sim_ui_menu_title      =1;
    vrep.sim_ui_menu_minimize   =2;
    vrep.sim_ui_menu_close      =4;
    vrep.sim_ui_menu_systemblock =8;

    % Boolean parameters
    vrep.sim_boolparam_hierarchy_visible                 =0;
    vrep.sim_boolparam_console_visible                   =1;
    vrep.sim_boolparam_collision_handling_enabled        =2;
    vrep.sim_boolparam_distance_handling_enabled         =3;
    vrep.sim_boolparam_ik_handling_enabled               =4;
    vrep.sim_boolparam_gcs_handling_enabled              =5;
    vrep.sim_boolparam_dynamics_handling_enabled         =6;
    vrep.sim_boolparam_joint_motion_handling_enabled     =7;
    vrep.sim_boolparam_path_motion_handling_enabled      =8;
    vrep.sim_boolparam_proximity_sensor_handling_enabled =9;
    vrep.sim_boolparam_vision_sensor_handling_enabled    =10;
    vrep.sim_boolparam_mill_handling_enabled             =11;
    vrep.sim_boolparam_browser_visible                   =12;
    vrep.sim_boolparam_scene_and_model_load_messages     =13;
    vrep.sim_reserved0                                   =14;
    vrep.sim_boolparam_shape_textures_are_visible        =15;
    vrep.sim_boolparam_display_enabled                   =16;
    vrep.sim_boolparam_infotext_visible                  =17;
    vrep.sim_boolparam_statustext_open                   =18;
    vrep.sim_boolparam_fog_enabled                       =19;
    vrep.sim_boolparam_rml2_available                    =20;
    vrep.sim_boolparam_rml4_available                    =21;
    vrep.sim_boolparam_mirrors_enabled                  =22;
    vrep.sim_boolparam_aux_clip_planes_enabled          =23;
    vrep.sim_boolparam_full_model_copy_from_api         =24;
    vrep.sim_boolparam_realtime_simulation              =25;
    vrep.sim_boolparam_force_show_wireless_emission     =27;
    vrep.sim_boolparam_force_show_wireless_reception    =28;
    vrep.sim_boolparam_video_recording_triggered        =29;
    vrep.sim_boolparam_threaded_rendering_enabled       =32;
    vrep.sim_boolparam_fullscreen                       =33;
    vrep.sim_boolparam_headless                         =34;
    vrep.sim_boolparam_hierarchy_toolbarbutton_enabled  =35;
    vrep.sim_boolparam_browser_toolbarbutton_enabled    =36;
    vrep.sim_boolparam_objectshift_toolbarbutton_enabled=37;
    vrep.sim_boolparam_objectrotate_toolbarbutton_enabled=38;
    vrep.sim_boolparam_force_calcstruct_all_visible     =39;
    vrep.sim_boolparam_force_calcstruct_all             =40;
    vrep.sim_boolparam_exit_request                     =41;
    vrep.sim_boolparam_play_toolbarbutton_enabled       =42;
    vrep.sim_boolparam_pause_toolbarbutton_enabled      =43;
    vrep.sim_boolparam_stop_toolbarbutton_enabled       =44;
    vrep.sim_boolparam_waiting_for_trigger              =45;

    % Integer parameters
    vrep.sim_intparam_error_report_mode      =0;
    vrep.sim_intparam_program_version        =1;
    vrep.sim_intparam_instance_count         =2;
    vrep.sim_intparam_custom_cmd_start_id    =3;
    vrep.sim_intparam_compilation_version    =4;
    vrep.sim_intparam_current_page           =5;
    vrep.sim_intparam_flymode_camera_handle  =6;
    vrep.sim_intparam_dynamic_step_divider   =7;
    vrep.sim_intparam_dynamic_engine         =8;
    vrep.sim_intparam_server_port_start      =9;
    vrep.sim_intparam_server_port_range      =10;
    vrep.sim_intparam_visible_layers         =11;
    vrep.sim_intparam_infotext_style         =12;
    vrep.sim_intparam_settings               =13;
    vrep.sim_intparam_edit_mode_type         =14;
    vrep.sim_intparam_server_port_next       =15;
    vrep.sim_intparam_qt_version             =16;
    vrep.sim_intparam_event_flags_read       =17;
    vrep.sim_intparam_event_flags_read_clear =18;
    vrep.sim_intparam_platform               =19;
    vrep.sim_intparam_scene_unique_id        =20;
    vrep.sim_intparam_work_thread_count      =21;
    vrep.sim_intparam_mouse_x                =22;
    vrep.sim_intparam_mouse_y                =23;
    vrep.sim_intparam_core_count             =24;
    vrep.sim_intparam_work_thread_calc_time_ms =25;
    vrep.sim_intparam_idle_fps               =26;
    vrep.sim_intparam_prox_sensor_select_down =27;
    vrep.sim_intparam_prox_sensor_select_up  =28;
    vrep.sim_intparam_stop_request_counter   =29;
    vrep.sim_intparam_program_revision       =30;
    vrep.sim_intparam_mouse_buttons          =31;
    vrep.sim_intparam_dynamic_warning_disabled_mask =32;
    vrep.sim_intparam_simulation_warning_disabled_mask =33;
    vrep.sim_intparam_scene_index            =34;
    vrep.sim_intparam_motionplanning_seed   =35;
    vrep.sim_intparam_speedmodifier         =36;


    % Float parameters
    vrep.sim_floatparam_rand=0;
    vrep.sim_floatparam_simulation_time_step=1;
    vrep.sim_floatparam_stereo_distance     =2;

    % String parameters
    vrep.sim_stringparam_application_path=0;
    vrep.sim_stringparam_video_filename=1;
    vrep.sim_stringparam_app_arg1           =2;
    vrep.sim_stringparam_app_arg2           =3;
    vrep.sim_stringparam_app_arg3           =4;
    vrep.sim_stringparam_app_arg4           =5;
    vrep.sim_stringparam_app_arg5           =6;
    vrep.sim_stringparam_app_arg6           =7;
    vrep.sim_stringparam_app_arg7           =8;
    vrep.sim_stringparam_app_arg8           =9;
    vrep.sim_stringparam_app_arg9           =10;
    vrep.sim_stringparam_scene_path_and_name    =13;

    % Array parameters
    vrep.sim_arrayparam_gravity          =0;
    vrep.sim_arrayparam_fog              =1;
    vrep.sim_arrayparam_fog_color        =2;
    vrep.sim_arrayparam_background_color1=3;
    vrep.sim_arrayparam_background_color2=4;
    vrep.sim_arrayparam_ambient_light    =5;
    vrep.sim_arrayparam_random_euler        =6;

    vrep.sim_objintparam_visibility_layer= 10;
    vrep.sim_objfloatparam_abs_x_velocity= 11;
    vrep.sim_objfloatparam_abs_y_velocity= 12;
    vrep.sim_objfloatparam_abs_z_velocity= 13;
    vrep.sim_objfloatparam_abs_rot_velocity= 14;
    vrep.sim_objfloatparam_objbbox_min_x= 15;
    vrep.sim_objfloatparam_objbbox_min_y= 16;
    vrep.sim_objfloatparam_objbbox_min_z= 17;
    vrep.sim_objfloatparam_objbbox_max_x= 18;
    vrep.sim_objfloatparam_objbbox_max_y= 19;
    vrep.sim_objfloatparam_objbbox_max_z= 20;
    vrep.sim_objfloatparam_modelbbox_min_x= 21;
    vrep.sim_objfloatparam_modelbbox_min_y= 22;
    vrep.sim_objfloatparam_modelbbox_min_z= 23;
    vrep.sim_objfloatparam_modelbbox_max_x= 24;
    vrep.sim_objfloatparam_modelbbox_max_y= 25;
    vrep.sim_objfloatparam_modelbbox_max_z= 26;
    vrep.sim_objintparam_collection_self_collision_indicator= 27;
    vrep.sim_objfloatparam_transparency_offset= 28;
    vrep.sim_objintparam_child_role= 29;
    vrep.sim_objintparam_parent_role= 30;
    vrep.sim_objintparam_manipulation_permissions= 31;
    vrep.sim_objintparam_illumination_handle= 32;

    vrep.sim_visionfloatparam_near_clipping= 1000;
    vrep.sim_visionfloatparam_far_clipping= 1001;
    vrep.sim_visionintparam_resolution_x= 1002;
    vrep.sim_visionintparam_resolution_y= 1003;
    vrep.sim_visionfloatparam_perspective_angle= 1004;
    vrep.sim_visionfloatparam_ortho_size= 1005;
    vrep.sim_visionintparam_disabled_light_components= 1006;
    vrep.sim_visionintparam_rendering_attributes= 1007;
    vrep.sim_visionintparam_entity_to_render= 1008;
    vrep.sim_visionintparam_windowed_size_x= 1009;
    vrep.sim_visionintparam_windowed_size_y= 1010;
    vrep.sim_visionintparam_windowed_pos_x= 1011;
    vrep.sim_visionintparam_windowed_pos_y= 1012;
    vrep.sim_visionintparam_pov_focal_blur= 1013;
    vrep.sim_visionfloatparam_pov_blur_distance= 1014;
    vrep.sim_visionfloatparam_pov_aperture= 1015;
    vrep.sim_visionintparam_pov_blur_sampled= 1016;
    vrep.sim_visionintparam_render_mode= 1017;

    vrep.sim_jointintparam_motor_enabled= 2000;
    vrep.sim_jointintparam_ctrl_enabled= 2001;
    vrep.sim_jointfloatparam_pid_p= 2002;
    vrep.sim_jointfloatparam_pid_i= 2003;
    vrep.sim_jointfloatparam_pid_d= 2004;
    vrep.sim_jointfloatparam_intrinsic_x= 2005;
    vrep.sim_jointfloatparam_intrinsic_y= 2006;
    vrep.sim_jointfloatparam_intrinsic_z= 2007;
    vrep.sim_jointfloatparam_intrinsic_qx= 2008;
    vrep.sim_jointfloatparam_intrinsic_qy= 2009;
    vrep.sim_jointfloatparam_intrinsic_qz= 2010;
    vrep.sim_jointfloatparam_intrinsic_qw= 2011;
    vrep.sim_jointfloatparam_velocity= 2012;
    vrep.sim_jointfloatparam_spherical_qx= 2013;
    vrep.sim_jointfloatparam_spherical_qy= 2014;
    vrep.sim_jointfloatparam_spherical_qz= 2015;
    vrep.sim_jointfloatparam_spherical_qw= 2016;
    vrep.sim_jointfloatparam_upper_limit= 2017;
    vrep.sim_jointfloatparam_kc_k= 2018;
    vrep.sim_jointfloatparam_kc_c= 2019;
    vrep.sim_jointfloatparam_ik_weight= 2021;
    vrep.sim_jointfloatparam_error_x= 2022;
    vrep.sim_jointfloatparam_error_y= 2023;
    vrep.sim_jointfloatparam_error_z= 2024;
    vrep.sim_jointfloatparam_error_a= 2025;
    vrep.sim_jointfloatparam_error_b= 2026;
    vrep.sim_jointfloatparam_error_g= 2027;
    vrep.sim_jointfloatparam_error_pos= 2028;
    vrep.sim_jointfloatparam_error_angle= 2029;
    vrep.sim_jointintparam_velocity_lock= 2030;
    vrep.sim_jointintparam_vortex_dep_handle= 2031;
    vrep.sim_jointfloatparam_vortex_dep_multiplication= 2032;
    vrep.sim_jointfloatparam_vortex_dep_offset= 2033;

    vrep.sim_shapefloatparam_init_velocity_x= 3000;
    vrep.sim_shapefloatparam_init_velocity_y= 3001;
    vrep.sim_shapefloatparam_init_velocity_z= 3002;
    vrep.sim_shapeintparam_static= 3003;
    vrep.sim_shapeintparam_respondable= 3004;
    vrep.sim_shapefloatparam_mass= 3005;
    vrep.sim_shapefloatparam_texture_x= 3006;
    vrep.sim_shapefloatparam_texture_y= 3007;
    vrep.sim_shapefloatparam_texture_z= 3008;
    vrep.sim_shapefloatparam_texture_a= 3009;
    vrep.sim_shapefloatparam_texture_b= 3010;
    vrep.sim_shapefloatparam_texture_g= 3011;
    vrep.sim_shapefloatparam_texture_scaling_x= 3012;
    vrep.sim_shapefloatparam_texture_scaling_y= 3013;
    vrep.sim_shapeintparam_culling= 3014;
    vrep.sim_shapeintparam_wireframe= 3015;
    vrep.sim_shapeintparam_compound= 3016;
    vrep.sim_shapeintparam_convex= 3017;
    vrep.sim_shapeintparam_convex_check= 3018;
    vrep.sim_shapeintparam_respondable_mask= 3019;
    vrep.sim_shapefloatparam_init_velocity_a= 3020;
    vrep.sim_shapefloatparam_init_velocity_b= 3021;
    vrep.sim_shapefloatparam_init_velocity_g= 3022;
    vrep.sim_shapestringparam_color_name= 3023;
    vrep.sim_shapeintparam_edge_visibility= 3024;
    vrep.sim_shapefloatparam_shading_angle= 3025;
    vrep.sim_shapefloatparam_edge_angle= 3026;
    vrep.sim_shapeintparam_edge_borders_hidden= 3027;

    vrep.sim_proxintparam_ray_invisibility= 4000;

    vrep.sim_forcefloatparam_error_x= 5000;
    vrep.sim_forcefloatparam_error_y= 5001;
    vrep.sim_forcefloatparam_error_z= 5002;
    vrep.sim_forcefloatparam_error_a= 5003;
    vrep.sim_forcefloatparam_error_b= 5004;
    vrep.sim_forcefloatparam_error_g= 5005;
    vrep.sim_forcefloatparam_error_pos= 5006;
    vrep.sim_forcefloatparam_error_angle= 5007;

    vrep.sim_lightintparam_pov_casts_shadows= 8000;

    vrep.sim_cameraintparam_disabled_light_components= 9000;
    vrep.sim_camerafloatparam_perspective_angle= 9001;
    vrep.sim_camerafloatparam_ortho_size= 9002;
    vrep.sim_cameraintparam_rendering_attributes= 9003;
    vrep.sim_cameraintparam_pov_focal_blur= 9004;
    vrep.sim_camerafloatparam_pov_blur_distance= 9005;
    vrep.sim_camerafloatparam_pov_aperture= 9006;
    vrep.sim_cameraintparam_pov_blur_samples= 9007;

    vrep.sim_dummyintparam_link_type= 10000;

    vrep.sim_mirrorfloatparam_width= 12000;
    vrep.sim_mirrorfloatparam_height= 12001;
    vrep.sim_mirrorfloatparam_reflectance= 12002;
    vrep.sim_mirrorintparam_enable= 12003;

    vrep.sim_pplanfloatparam_x_min= 20000;
    vrep.sim_pplanfloatparam_x_range= 20001;
    vrep.sim_pplanfloatparam_y_min= 20002;
    vrep.sim_pplanfloatparam_y_range= 20003;
    vrep.sim_pplanfloatparam_z_min= 20004;
    vrep.sim_pplanfloatparam_z_range= 20005;
    vrep.sim_pplanfloatparam_delta_min= 20006;
    vrep.sim_pplanfloatparam_delta_range= 20007;

    vrep.sim_mplanintparam_nodes_computed= 25000;
    vrep.sim_mplanintparam_prepare_nodes= 25001;
    vrep.sim_mplanintparam_clear_nodes= 25002;

    % User interface elements
    vrep.sim_gui_menubar                        =1;
    vrep.sim_gui_popups                     =2;
    vrep.sim_gui_toolbar1                   =4;
    vrep.sim_gui_toolbar2                   =8;
    vrep.sim_gui_hierarchy                  =16;
    vrep.sim_gui_infobar                        =32;
    vrep.sim_gui_statusbar                  =64;
    vrep.sim_gui_scripteditor               =128;
    vrep.sim_gui_scriptsimulationparameters =256;
    vrep.sim_gui_dialogs                        =512;
    vrep.sim_gui_browser                        =1024;
    vrep.sim_gui_all                            =65535;

    % Joint modes
    vrep.sim_jointmode_passive       =0;
    vrep.sim_jointmode_motion        =1;
    vrep.sim_jointmode_ik            =2;
    vrep.sim_jointmode_ikdependent   =3;
    vrep.sim_jointmode_dependent     =4;
    vrep.sim_jointmode_force         =5;

    % Navigation and selection modes with the mouse.
    vrep.sim_navigation_passive                 =0;
    vrep.sim_navigation_camerashift             =1;
    vrep.sim_navigation_camerarotate                =2;
    vrep.sim_navigation_camerazoom              =3;
    vrep.sim_navigation_cameratilt              =4;
    vrep.sim_navigation_cameraangle             =5;
    vrep.sim_navigation_camerafly               =6;
    vrep.sim_navigation_objectshift             =7;
    vrep.sim_navigation_objectrotate                =8;
    vrep.sim_navigation_reserved2               =9;
    vrep.sim_navigation_reserved3               =10;
    vrep.sim_navigation_jointpathtest           =11;
    vrep.sim_navigation_ikmanip                 =12;
    vrep.sim_navigation_objectmultipleselection =13;

    vrep.sim_navigation_reserved4               =256;
    vrep.sim_navigation_clickselection          =512;
    vrep.sim_navigation_ctrlselection           =1024;
    vrep.sim_navigation_shiftselection          =2048;
    vrep.sim_navigation_camerazoomwheel         =4096;
    vrep.sim_navigation_camerarotaterightbutton =8192;

    % Remote API message header structure
    vrep.simx_headeroffset_crc           =0;
    vrep.simx_headeroffset_version       =2;
    vrep.simx_headeroffset_message_id    =3;
    vrep.simx_headeroffset_client_time   =7;
    vrep.simx_headeroffset_server_time   =11;
    vrep.simx_headeroffset_scene_id      =15;
    vrep.simx_headeroffset_server_state  =17;

    % Remote API command header
    vrep.simx_cmdheaderoffset_mem_size       =0;
    vrep.simx_cmdheaderoffset_full_mem_size  =4;
    vrep.simx_cmdheaderoffset_pdata_offset0  =8;
    vrep.simx_cmdheaderoffset_pdata_offset1  =10;
    vrep.simx_cmdheaderoffset_cmd           =14;
    vrep.simx_cmdheaderoffset_delay_or_split =18;
    vrep.simx_cmdheaderoffset_sim_time       =20;
    vrep.simx_cmdheaderoffset_status         =24;
    vrep.simx_cmdheaderoffset_reserved       =25;

    % Regular operation modes
    vrep.simx_opmode_oneshot                =0;
    vrep.simx_opmode_blocking           =65536;
    vrep.simx_opmode_oneshot_wait       =65536;
    vrep.simx_opmode_continuous         =131072;
    vrep.simx_opmode_streaming          =131072;

    % Operation modes for heavy data
    vrep.simx_opmode_oneshot_split      =196608;
    vrep.simx_opmode_continuous_split   =262144;
    vrep.simx_opmode_streaming_split        =262144;

    % Special operation modes
    vrep.simx_opmode_discontinue            =327680;
    vrep.simx_opmode_buffer             =393216;
    vrep.simx_opmode_remove             =458752;

    % Command return codes
    vrep.simx_return_ok                     =0;
    vrep.simx_return_novalue_flag           =1;
    vrep.simx_return_timeout_flag           =2;
    vrep.simx_return_illegal_opmode_flag    =4;
    vrep.simx_return_remote_error_flag      =8;
    vrep.simx_return_split_progress_flag    =16;
    vrep.simx_return_local_error_flag       =32;
    vrep.simx_return_initialize_error_flag  =64;

    % Following for backward compatibility (same as above)
    vrep.simx_error_noerror                 =0;
    vrep.simx_error_novalue_flag            =1;
    vrep.simx_error_timeout_flag            =2;
    vrep.simx_error_illegal_opmode_flag     =4;
    vrep.simx_error_remote_error_flag       =8;
    vrep.simx_error_split_progress_flag     =16;
    vrep.simx_error_local_error_flag        =32;
    vrep.simx_error_initialize_error_flag   =64;

    %load functions
    octfile = strcat(pwd,"//remApi.oct");
    autoload("simxStart",octfile);
    autoload("simxFinish",octfile);
    autoload("simxAddStatusbarMessage",octfile);
    autoload("simxAppendStringSignal",octfile);
    autoload("simxWriteStringStream",octfile);
    autoload("simxAuxiliaryConsoleClose",octfile);
    autoload("simxAuxiliaryConsoleOpen",octfile);
    autoload("simxAuxiliaryConsolePrint",octfile);
    autoload("simxAuxiliaryConsoleShow",octfile);
    autoload("simxBreakForceSensor",octfile);
    autoload("simxClearFloatSignal",octfile);
    autoload("simxClearIntegerSignal",octfile);
    autoload("simxClearStringSignal",octfile);
    autoload("simxCloseScene",octfile);
    autoload("simxCopyPasteObjects",octfile);
    autoload("simxCreateBuffer",octfile);
    autoload("simxCreateDummy",octfile);
    autoload("simxDisplayDialog",octfile);
    autoload("simxEndDialog",octfile);
    autoload("simxEraseFile",octfile);
    autoload("simxGetAndClearStringSignal",octfile);
    autoload("simxReadStringStream",octfile);
    autoload("simxGetArrayParameter",octfile);
    autoload("simxGetBooleanParameter",octfile);
    autoload("simxGetCollisionHandle",octfile);
    autoload("simxGetCollectionHandle",octfile);
    autoload("simxGetConnectionId",octfile);
    autoload("simxGetDialogInput",octfile);
    autoload("simxGetDialogResult",octfile);
    autoload("simxGetDistanceHandle",octfile);
    autoload("simxGetFloatingParameter",octfile);
    autoload("simxGetFloatSignal",octfile);
    autoload("simxGetInMessageInfo",octfile);
    autoload("simxGetIntegerParameter",octfile);
    autoload("simxGetIntegerSignal",octfile);
    autoload("simxGetJointMatrix",octfile);
    autoload("simxGetJointPosition",octfile);
    autoload("simxGetLastCmdTime",octfile);
    autoload("simxGetLastErrors",octfile);
    autoload("simxGetModelProperty",octfile);
    autoload("simxGetObjectChild",octfile);
    autoload("simxGetObjectFloatParameter",octfile);
    autoload("simxGetObjectGroupData",octfile);
    autoload("simxCallScriptFunction",octfile);
    autoload("simxGetObjectHandle",octfile);
    autoload("simxGetObjectIntParameter",octfile);
    autoload("simxGetObjectOrientation",octfile);
    autoload("simxGetObjectQuaternion",octfile);
    autoload("simxGetObjectParent",octfile);
    autoload("simxGetObjectPosition",octfile);
    autoload("simxGetObjects",octfile);
    autoload("simxGetObjectSelection",octfile);
    autoload("simxGetObjectVelocity",octfile);
    autoload("simxGetOutMessageInfo",octfile);
    autoload("simxGetPingTime",octfile);
    autoload("simxGetStringParameter",octfile);
    autoload("simxGetStringSignal",octfile);
    autoload("simxGetUIButtonProperty",octfile);
    autoload("simxGetUIEventButton",octfile);
    autoload("simxGetUIHandle",octfile);
    autoload("simxGetUISlider",octfile);
    autoload("simxGetVisionSensorDepthBuffer",octfile);
    autoload("simxGetVisionSensorImage",octfile);
    autoload("simxGetJointForce",octfile);
    autoload("simxJointGetForce",octfile);
    autoload("simxLoadModel",octfile);
    autoload("simxLoadScene",octfile);
    autoload("simxLoadUI",octfile);
    autoload("simxPauseCommunication",octfile);
    autoload("simxPauseSimulation",octfile);
    autoload("simxQuery",octfile);
    autoload("simxReadCollision",octfile);
    autoload("simxReadDistance",octfile);
    autoload("simxReadForceSensor",octfile);
    autoload("simxReadProximitySensor",octfile);
    autoload("simxReadVisionSensor",octfile);
    autoload("simxReleaseBuffer",octfile);
    autoload("simxRemoveObject",octfile);
    autoload("simxRemoveModel",octfile);
    autoload("simxRemoveUI",octfile);
    autoload("simxSetArrayParameter",octfile);
    autoload("simxSetBooleanParameter",octfile);
    autoload("simxSetFloatingParameter",octfile);
    autoload("simxSetFloatSignal",octfile);
    autoload("simxSetIntegerParameter",octfile);
    autoload("simxSetIntegerSignal",octfile);
    autoload("simxSetJointForce",octfile);
    autoload("simxSetJointPosition",octfile);
    autoload("simxSetJointTargetPosition",octfile);
    autoload("simxSetJointTargetVelocity",octfile);
    autoload("simxSetModelProperty",octfile);
    autoload("simxSetObjectFloatParameter",octfile);
    autoload("simxSetObjectIntParameter",octfile);
    autoload("simxSetObjectOrientation",octfile);
    autoload("simxSetObjectQuaternion",octfile);
    autoload("simxSetObjectParent",octfile);
    autoload("simxSetObjectPosition",octfile);
    autoload("simxSetObjectSelection",octfile);
    autoload("simxSetSphericalJointMatrix",octfile);
    autoload("simxSetStringSignal",octfile);
    autoload("simxSetUIButtonLabel",octfile);
    autoload("simxSetUIButtonProperty",octfile);
    autoload("simxSetUISlider",octfile);
    autoload("simxSetVisionSensorImage",octfile);
    autoload("simxStartSimulation",octfile);
    autoload("simxStopSimulation",octfile);
    autoload("simxSynchronous",octfile);
    autoload("simxSynchronousTrigger",octfile);
    autoload("simxTransferFile",octfile);
    autoload("simxPackFloats",octfile);
    autoload("simxPackInts",octfile);
    autoload("simxUnpackFloats",octfile);
    autoload("simxUnpackInts",octfile);
end
