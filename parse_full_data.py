# Let's extract the raw prompt text for the full 414 logs and tickets
import re
import json
from collections import defaultdict, Counter
from datetime import datetime

# Read from prompt text or write raw text
with open('/Users/franciscomateus/Documents/DashboardUMB/raw_data.txt', 'r') as f:
    text = f.read()

# Let's append the 414 events
events_raw = """45691880086,PRUEBA FRANCISCO (test),Estudios,2026-07-02 19:03:06
45691880086,PRUEBA FRANCISCO (test),Estudios,2026-07-02 19:16:44
45705605243,BLUEPRISM NARNAJA PRUEBA 2 (test),Estudios,2026-07-02 19:18:48
45705605243,BLUEPRISM NARNAJA PRUEBA 2 (test),Estudios,2026-07-02 19:22:51
46719717891,John Arley,Estudios,2026-07-15 12:22:26
46719717891,John Arley,Estudios,2026-07-16 13:05:42
46719717891,John Arley,Estudios,2026-07-17 14:06:28
46719717891,John Arley,Estudios,2026-07-22 12:13:08
46724480844,Diana Carolina,Estudios,2026-07-14 16:27:56
46724480844,Diana Carolina,Estudios,2026-07-15 12:34:28
46739778711,Yesica Marcela,Estudios,2026-07-15 12:35:41
46740667214,Issy Edith,Estudios,2026-07-15 12:23:57
46740667214,Issy Edith,Estudios,2026-07-16 13:07:08
46740667214,Issy Edith,Estudios,2026-07-17 14:07:58
46740667214,Issy Edith,Estudios,2026-07-22 12:14:37
46740676950,Martínez Sánchez,Estudios,2026-07-15 12:27:58
46740777394,Rojas Reyes,Estudios,2026-07-15 12:30:08
46740777904,Sara Valentina,Estudios,2026-07-15 12:31:37
46741120821,Alejandro,Estudios,2026-07-15 12:33:07
46741120821,Alejandro,Estudios,2026-07-16 13:08:34
46741120821,Alejandro,Estudios,2026-07-17 14:09:28
46741120821,Alejandro,Estudios,2026-07-22 12:15:59
46755070819,Garnica Daza,Estudios,2026-07-16 13:15:30
46756611613,Jorge Eduardo,Estudios,2026-07-16 13:13:31
46757072207,Perilla Orjuela,Estudios,2026-07-16 13:10:34
46757072207,Perilla Orjuela,Estudios,2026-07-17 14:16:26
46757072207,Perilla Orjuela,Estudios,2026-07-22 12:18:00
46757389167,Isabella,Estudios,2026-07-16 13:16:59
46771819267,Yessika,Estudios,2026-07-16 13:12:02
46811412400,Hector Fabio,Estudios,2026-07-17 14:17:26
46811412400,Hector Fabio,Estudios,2026-07-22 12:21:23
46816991784,Maria Camila,Estudios,2026-07-17 14:10:56
46825182643,Adriana Lorena,Estudios,2026-07-17 14:19:29
46834756208,Juan Nicolas,Estudios,2026-07-22 12:20:00
46836750441,Avendaño Gutiérrez,Estudios,2026-07-17 14:14:24
46844468821,Maria Angelica,Estudios,2026-07-22 12:19:00
46844468821,Maria Angelica,Estudios,2026-07-24 12:36:10
46844468821,Maria Angelica,Estudios,2026-07-27 15:10:24
46844468821,Maria Angelica,Estudios,2026-07-28 13:16:50
46846342757,Andres Felipe,Estudios,2026-07-17 14:20:27
46850507622,Maria Alejandra,Estudios,2026-07-17 14:18:31
46953253529,John Alexander,Estudios,2026-07-22 12:22:44
46953253529,John Alexander,Estudios,2026-07-24 12:49:44
47010684030,Nubia,Estudios,2026-07-22 12:28:55
47012693680,Alejandra,Estudios,2026-07-22 12:30:24
47012999439,Bogota Jimenez,Estudios,2026-07-22 12:24:47
47022974724,Monica Marcela,Estudios,2026-07-22 12:27:33
47034353585,Michael,Estudios,2026-07-22 12:26:11
47034353585,Michael,Estudios,2026-07-24 12:37:35
47034353585,Michael,Estudios,2026-07-27 15:11:52
47034353585,Michael,Estudios,2026-07-28 13:18:10
47052252319,Muñoz,Estudios,2026-07-22 12:32:25
47071391394,Sara,Estudios,2026-07-24 12:51:04
47072013216,Kamila / Suárez,Estudios,2026-07-24 12:56:54
47072013216,Kamila / Suárez,Estudios,2026-07-27 15:26:34
47072013216,Kamila / Suárez,Estudios,2026-07-28 13:31:28
47072150305,Suárez,Estudios,2026-07-22 12:41:23
47073234321,García Lozano,Estudios,2026-07-22 12:37:54
47073543096,Ospina Contreras,Estudios,2026-07-22 12:34:28
47081750277,Aviles Reina,Estudios,2026-07-22 12:43:25
47085918779,Anderson Santiago,Estudios,2026-07-22 12:35:51
47088722544,Dylan Mauricio / Sanchez Martinez,Estudios,2026-07-24 12:53:17
47088722544,Dylan Mauricio / Sanchez Martinez,Estudios,2026-07-27 15:25:35
47088722544,Dylan Mauricio / Sanchez Martinez,Estudios,2026-07-28 13:30:30
47091803039,Jessica Andrea,Estudios,2026-07-22 12:39:23
47091803039,Jessica Andrea,Estudios,2026-07-24 12:38:09
47091803039,Jessica Andrea,Estudios,2026-07-27 15:13:14
47091803039,Jessica Andrea,Estudios,2026-07-28 13:19:24
47093042091,Montes Alvarez,Estudios,2026-07-22 12:45:26
47093352754,Chamorro,Estudios,2026-07-22 12:47:28
47097674603,Celis Mafla,Estudios,2026-07-24 12:43:59
47097674603,Celis Mafla,Estudios,2026-07-27 15:19:46
47097674603,Celis Mafla,Estudios,2026-07-28 13:24:54
47097829260,Juan Camilo,Estudios,2026-07-24 12:39:53
47097829260,Juan Camilo,Estudios,2026-07-27 15:16:13
47097829260,Juan Camilo,Estudios,2026-07-28 13:21:56
47100640426,Arcos Martinez,Estudios,2026-07-24 13:21:05
47105416474,Juan Camilo,Estudios,2026-07-24 12:41:38
47105416474,Juan Camilo,Estudios,2026-07-27 15:17:44
47105416474,Juan Camilo,Estudios,2026-07-28 13:23:14
47106346067,Diego Alejandro,Estudios,2026-07-24 12:58:14
47107142714,María Camila,Estudios,2026-07-24 13:24:44
47108868715,Danna / Rodriguez,Estudios,2026-07-27 15:29:11
47108868715,Danna / Rodriguez,Estudios,2026-07-28 13:32:25
47111488652,Alejandra,Estudios,2026-07-24 12:54:51
47111488652,Alejandra,Estudios,2026-07-27 15:14:43
47111488652,Alejandra,Estudios,2026-07-28 13:20:39
47116949790,Mariyenci,Estudios,2026-07-27 15:24:40
47116949790,Mariyenci,Estudios,2026-07-28 13:28:39
47120362291,Maia Ximena,Estudios,2026-07-27 15:23:44
47120362291,Maia Ximena,Estudios,2026-07-28 13:27:43
47121900563,Nieto Ayala,Estudios,2026-07-24 13:00:17
47124372288,Sofia,Estudios,2026-07-24 12:44:42
47124372288,Sofia,Estudios,2026-07-27 15:20:35
47124372288,Sofia,Estudios,2026-07-28 13:25:50
47127950715,Pulido Ballesteros,Estudios,2026-07-24 13:23:09
47135387009,Kelly,Estudios,2026-07-24 12:46:12
47138733591,Valeria / Cediel Alonso,Estudios,2026-07-24 12:48:17
47138733591,Valeria / Cediel Alonso,Estudios,2026-07-27 15:22:47
47138733591,Valeria / Cediel Alonso,Estudios,2026-07-28 13:26:46
47144168220,Juan David,Estudios,2026-07-27 15:30:26
47144168220,Juan David,Estudios,2026-07-28 13:33:21
47175154467,Luisa Cilvana,Estudios,2026-07-27 15:32:49
47175154467,Luisa Cilvana,Estudios,2026-07-28 13:34:18
47182985734,Mery,Estudios,2026-07-28 13:29:34
47201888596,Luengas Ariza,Estudios,2026-07-28 13:40:46
47205357477,Martinez Bedoya,Estudios,2026-07-28 13:42:32
47208751254,Andrés,Estudios,2026-07-27 15:35:39
47208751254,Andrés,Estudios,2026-07-28 13:35:12
47210908498,Valery Sofía,Estudios,2026-07-27 15:36:52
47210908498,Valery Sofía,Estudios,2026-07-28 13:36:09
47213549873,Maryi,Estudios,2026-07-28 13:45:03
47214160686,Juan David / Ramírez Vargas,Estudios,2026-07-27 15:38:31
47214160686,Juan David / Ramírez Vargas,Estudios,2026-07-28 13:37:05
47215383310,María Fernanda,Estudios,2026-07-28 13:43:49
47218646886,Juan Sebastian,Estudios,2026-07-28 13:38:59
47226956348,Paula Valentina,Estudios,2026-07-28 13:38:03
47231136793,Carlos Hennry,Estudios,2026-07-28 13:57:36
47235453622,Yerson,Estudios,2026-07-28 13:49:17
47238845072,Ruiz Mena,Estudios,2026-07-28 13:59:19
47240884111,Isabela,Estudios,2026-07-28 13:48:02
47244446304,Picon Garcia,Estudios,2026-07-28 13:51:00
47246622998,Moreno Ramos,Estudios,2026-07-28 13:46:46
47253609764,Pineda,Estudios,2026-07-28 13:54:31
47256551483,Camacho Orobio,Estudios,2026-07-28 13:52:44
47256551602,Forero Vergara,Estudios,2026-07-28 13:56:19
47968411215,Francy Helena,Estudios,2026-09-17 11:04:30
47968411215,Francy Helena,Estudios,2026-09-17 13:04:35
47968411215,Francy Helena,Estudios,2026-09-17 14:11:27
47968411215,Francy Helena,Estudios,2026-09-17 16:00:12
47968411215,Francy Helena,Estudios,2026-09-17 17:04:27
48140072207,Juan Jose,Estudios,2026-09-04 19:00:36
48148153611,Hanna Valeria,Estudios,2026-09-04 19:03:35
48214520074,Juana,Estudios,2026-09-04 19:02:05
48234145688,Cuadros Rincon,Estudios,2026-09-04 18:51:40
48238184488,Brito Rangel,Estudios,2026-09-04 18:56:28
48245175186,Oramas Reyes,Estudios,2026-09-08 17:36:02
48285990934,Juan David,Estudios,2026-09-08 17:28:09
48285990934,Juan David,Estudios,2026-09-08 17:29:19
48285990934,Juan David,Estudios,2026-09-08 21:18:17
48285990934,Juan David,Estudios,2026-09-09 22:55:56
48285990934,Juan David,Estudios,2026-09-10 01:01:28
48285990934,Juan David,Estudios,2026-09-10 01:06:41
48285990934,Juan David,Estudios,2026-09-10 13:04:11
48285990934,Juan David,Estudios,2026-09-10 15:05:13
48299028153,Wilson Andres Carrillo Ortiz,Estudios,2026-09-08 17:31:11
48299028153,Wilson Andres Carrillo Ortiz,Estudios,2026-09-08 21:19:41
48299028153,Wilson Andres Carrillo Ortiz,Estudios,2026-09-09 15:50:34
48299028153,Wilson Andres Carrillo Ortiz,Estudios,2026-09-09 17:22:02
48299028153,Wilson Andres Carrillo Ortiz,Estudios,2026-09-09 19:52:04
48299028153,Wilson Andres Carrillo Ortiz,Estudios,2026-09-09 22:47:35
48299028153,Wilson Andres Carrillo Ortiz,Estudios,2026-09-10 00:35:14
48313821877,Fonseca Ardila,Estudios,2026-09-08 17:39:50
48346161807,Cuadros Rincon,Estudios,2026-09-08 17:43:18
48347709365,Pablo Andres,Estudios,2026-09-08 17:41:30
48356259181,Paola Andrea,Estudios,2026-09-08 17:44:54
48362206040,Rufina,Estudios,2026-09-08 17:48:08
48362210715,Nubia,Estudios,2026-09-09 15:53:26
48362210715,Nubia,Estudios,2026-09-09 17:24:54
48372664355,Melany Sofia,Estudios,2026-09-08 21:25:24
48372664355,Melany Sofia,Estudios,2026-09-10 13:05:12
48372664355,Melany Sofia,Estudios,2026-09-10 15:06:18
48372664355,Melany Sofia,Estudios,2026-09-10 17:05:11
48372664355,Melany Sofia,Estudios,2026-09-10 19:05:21
48372664355,Melany Sofia,Estudios,2026-09-10 21:05:16
48373377312,Gaona Trompa,Estudios,2026-09-08 21:28:56
48373995312,Alexander,Estudios,2026-09-08 21:26:48
48373995312,Alexander,Estudios,2026-09-09 13:12:02
48373995312,Alexander,Estudios,2026-09-09 15:58:41
48378476317,Andrade Moreno,Estudios,2026-09-08 21:21:32
48380807068,Quijano Mejia,Estudios,2026-09-08 17:46:42
48382366624,Peña Pedraza,Estudios,2026-09-08 21:34:49
48385893194,Herrera Javela,Estudios,2026-09-08 21:38:14
48404554605,Sánchez Espejo / María Catalina,Estudios,2026-09-08 21:31:40
48404554605,Sánchez Espejo / María Catalina,Estudios,2026-09-09 13:14:27
48436156825,Yuleidis Modesta,Estudios,2026-09-10 23:08:26
48436156825,Yuleidis Modesta,Estudios,2026-09-11 11:08:13
48436156825,Yuleidis Modesta,Estudios,2026-09-11 13:08:29
48436301439,Joaquin Andres Tabares Pérez,Estudios,2026-09-12 17:05:13
48436301439,Joaquin Andres Tabares Pérez,Estudios,2026-09-12 19:05:09
48436301439,Joaquin Andres Tabares Pérez,Estudios,2026-09-12 21:05:12
48436301439,Joaquin Andres Tabares Pérez,Estudios,2026-09-12 23:05:12
48436301439,Joaquin Andres Tabares Pérez,Estudios,2026-09-13 11:05:08
48436301439,Joaquin Andres Tabares Pérez,Estudios,2026-09-14 15:23:56
48436301439,Joaquin Andres Tabares Pérez,Estudios,2026-09-14 18:58:21
48436301439,Joaquin Andres Tabares Pérez,Estudios,2026-09-14 19:45:12
48436301439,Joaquin Andres Tabares Pérez,Estudios,2026-09-14 21:05:44
48436301439,Joaquin Andres Tabares Pérez,Estudios,2026-09-16 02:47:45
48436301439,Joaquin Andres Tabares Pérez,Estudios,2026-09-16 11:04:55
48436301439,Joaquin Andres Tabares Pérez,Estudios,2026-09-16 13:04:59
48436301439,Joaquin Andres Tabares Pérez,Estudios,2026-09-16 15:07:04
48436301439,Joaquin Andres Tabares Pérez,Estudios,2026-09-16 16:46:58
48436301439,Joaquin Andres Tabares Pérez,Estudios,2026-09-16 16:54:03
48436433832,Prieto Espitia,Estudios,2026-09-09 16:01:03
48438699892,Katherine Orjuela Bischoff,Estudios,2026-09-09 17:27:47
48440431959,Juan Daniel,Estudios,2026-09-10 21:11:17
48440431959,Juan Daniel,Estudios,2026-09-10 23:06:23
48440431959,Juan Daniel,Estudios,2026-09-11 11:06:12
48440431959,Juan Daniel,Estudios,2026-09-11 13:06:24
48441892192,Magnolia Rocio,Estudios,2026-09-09 17:26:18
48441892192,Magnolia Rocio,Estudios,2026-09-10 00:38:19
48441892192,Magnolia Rocio,Estudios,2026-09-10 01:09:44
48441892192,Magnolia Rocio,Estudios,2026-09-10 13:07:12
48445587985,Elizabeth Del Carmen,Estudios,2026-09-10 23:11:29
48445587985,Elizabeth Del Carmen,Estudios,2026-09-11 11:11:14
48445587985,Elizabeth Del Carmen,Estudios,2026-09-11 13:11:37
48446515893,Yuleidis Modesta,Estudios,2026-09-10 21:09:17
48450536977,Juan,Estudios,2026-09-10 17:07:17
48452879760,Victor Manuel,Estudios,2026-09-11 15:07:36
48453264824,María,Estudios,2026-09-09 16:07:50
48456793353,Forero Ruano,Estudios,2026-09-09 15:55:47
48458187785,Cuadros Rincon,Estudios,2026-09-09 16:04:12
48458507616,Rocío Esmeralda,Estudios,2026-09-10 00:41:41
48458507616,Rocío Esmeralda,Estudios,2026-09-10 01:10:46
48458507616,Rocío Esmeralda,Estudios,2026-09-10 13:08:14
48459117221,Luis David,Estudios,2026-09-09 16:09:18
48463323277,Jorge Armando,Estudios,2026-09-10 15:09:21
48463483255,Julian Esteban,Estudios,2026-09-10 19:09:29
48463483255,Julian Esteban,Estudios,2026-09-11 15:06:33
48463951013,Juan Camilo,Estudios,2026-09-10 17:08:20
48463951013,Juan Camilo,Estudios,2026-09-10 19:07:27
48463951013,Juan Camilo,Estudios,2026-09-10 21:08:17
48465997663,Juan Karlos Cardenas Rincon,Estudios,2026-09-09 22:49:53
48465997663,Juan Karlos Cardenas Rincon,Estudios,2026-09-10 00:40:10
48467588011,Victor Manuel Castillo Amado,Estudios,2026-09-12 17:06:15
48467588011,Victor Manuel Castillo Amado,Estudios,2026-09-12 19:06:10
48467588011,Victor Manuel Castillo Amado,Estudios,2026-09-12 21:06:14
48467588011,Victor Manuel Castillo Amado,Estudios,2026-09-12 23:06:15
48467588011,Victor Manuel Castillo Amado,Estudios,2026-09-13 11:06:09
48467588011,Victor Manuel Castillo Amado,Estudios,2026-09-14 15:25:00
48467588011,Victor Manuel Castillo Amado,Estudios,2026-09-14 19:00:30
48467588011,Victor Manuel Castillo Amado,Estudios,2026-09-14 19:47:17
48467588011,Victor Manuel Castillo Amado,Estudios,2026-09-14 21:09:19
48467588011,Victor Manuel Castillo Amado,Estudios,2026-09-15 23:12:14
48467588011,Victor Manuel Castillo Amado,Estudios,2026-09-16 03:35:41
48467588011,Victor Manuel Castillo Amado,Estudios,2026-09-16 11:05:38
48467588011,Victor Manuel Castillo Amado,Estudios,2026-09-16 13:05:43
48467588011,Victor Manuel Castillo Amado,Estudios,2026-09-16 15:09:21
48467588011,Victor Manuel Castillo Amado,Estudios,2026-09-16 16:55:54
48468037018,Fabian Felipe,Estudios,2026-09-10 23:09:27
48468037018,Fabian Felipe,Estudios,2026-09-11 11:09:13
48468037018,Fabian Felipe,Estudios,2026-09-11 13:09:33
48535204013,Paula Katherine,Estudios,2026-09-11 19:09:24
48549884728,Dilan Santiago,Estudios,2026-09-11 19:08:21
48551796367,Patricia Arelis,Estudios,2026-09-14 19:04:45
48556186660,Paula Vanesa,Estudios,2026-09-16 15:18:04
48559282988,Leidy,Estudios,2026-09-16 17:10:02
48559282988,Leidy,Estudios,2026-09-16 19:07:47
48559417245,Magnolia Rocio Lara Gualteros,Estudios,2026-09-16 03:34:08
48559417245,Magnolia Rocio Lara Gualteros,Estudios,2026-09-16 11:07:57
48559417245,Magnolia Rocio Lara Gualteros,Estudios,2026-09-16 13:08:03
48559417245,Magnolia Rocio Lara Gualteros,Estudios,2026-09-16 15:14:21
48559417245,Magnolia Rocio Lara Gualteros,Estudios,2026-09-16 17:08:21
48560982075,Gustavo Gomez Castellanos,Estudios,2026-09-16 15:05:40
48560982075,Gustavo Gomez Castellanos,Estudios,2026-09-16 16:29:57
48561713419,Wilmer,Estudios,2026-09-14 19:01:57
48567834265,Haider Camilo,Estudios,2026-09-12 17:09:18
48567834265,Haider Camilo,Estudios,2026-09-12 19:09:10
48567834265,Haider Camilo,Estudios,2026-09-12 21:09:17
48567834265,Haider Camilo,Estudios,2026-09-12 23:09:20
48567834265,Haider Camilo,Estudios,2026-09-13 11:09:11
48568507208,Karol Yaneth,Estudios,2026-09-14 21:12:53
48571617721,Santiago Velasco Bacca,Estudios,2026-09-15 15:09:07
48571617721,Santiago Velasco Bacca,Estudios,2026-09-15 19:08:54
48571617721,Santiago Velasco Bacca,Estudios,2026-09-15 21:08:49
48571617721,Santiago Velasco Bacca,Estudios,2026-09-15 23:08:53
48571617721,Santiago Velasco Bacca,Estudios,2026-09-16 03:32:02
48571618675,Córdoba,Horarios,2026-09-16 04:27:25
48573617474,Marvin,Estudios,2026-09-15 11:12:18
48575359767,Juan David Velasquez Rojas,Estudios,2026-09-16 17:11:45
48575360391,Maria Camila Peralta Perez,Estudios,2026-09-16 17:14:06
48575576382,Valerin Yadira,Estudios,2026-09-12 17:08:16
48575576382,Valerin Yadira,Estudios,2026-09-12 19:08:11
48575576382,Valerin Yadira,Estudios,2026-09-12 21:08:16
48575576382,Valerin Yadira,Estudios,2026-09-12 23:08:16
48575576382,Valerin Yadira,Estudios,2026-09-13 11:08:10
48577974328,Andres Grueso Balanta,Estudios,2026-09-14 19:51:44
48577974328,Andres Grueso Balanta,Estudios,2026-09-14 21:10:38
48577974328,Andres Grueso Balanta,Estudios,2026-09-16 03:37:12
48577974328,Andres Grueso Balanta,Estudios,2026-09-16 11:06:24
48577974328,Andres Grueso Balanta,Estudios,2026-09-16 13:06:30
48577974328,Andres Grueso Balanta,Estudios,2026-09-16 15:10:40
48577974328,Andres Grueso Balanta,Estudios,2026-09-16 17:05:51
48579397665,Mateo,Estudios,2026-09-15 21:15:41
48581708621,Juan Diego,Estudios,2026-09-15 15:13:50
48584522855,Daniel Esteban Castro Reyes,Estudios,2026-09-16 23:06:32
48584522855,Daniel Esteban Castro Reyes,Estudios,2026-09-17 11:06:29
48584522855,Daniel Esteban Castro Reyes,Estudios,2026-09-17 13:06:36
48584522855,Daniel Esteban Castro Reyes,Estudios,2026-09-17 14:25:21
48584522855,Daniel Esteban Castro Reyes,Estudios,2026-09-17 17:07:21
48584522855,Daniel Esteban Castro Reyes,Estudios,2026-09-17 18:32:49
48585270172,Juan Camilo Borja Vélez,Estudios,2026-09-14 21:07:01
48585270172,Juan Camilo Borja Vélez,Estudios,2026-09-16 02:51:41
48585270172,Juan Camilo Borja Vélez,Estudios,2026-09-16 11:07:08
48585270172,Juan Camilo Borja Vélez,Estudios,2026-09-16 13:07:13
48585270172,Juan Camilo Borja Vélez,Estudios,2026-09-16 15:12:58
48585270172,Juan Camilo Borja Vélez,Estudios,2026-09-16 17:07:03
48587362874,Michael Lozano González,Estudios,2026-09-16 17:16:23
48587517974,Emelin Dayana Bonett Rojas,Estudios,2026-09-16 17:17:51
48588409892,Andrea,Estudios,2026-09-14 15:26:04
48588419866,Johan Sebastian,Estudios,2026-09-15 11:13:31
48589823005,Paula Nathaly,Estudios,2026-09-14 19:49:44
48590621214,David Santiago,Horarios,2026-09-19 15:08:26
48590621214,David Santiago,Horarios,2026-09-19 19:08:40
48590621214,David Santiago,Horarios,2026-09-19 21:08:25
48590621214,David Santiago,Horarios,2026-09-21 13:08:22
48591855901,Juan Diego,Estudios,2026-09-15 15:16:02
48591855901,Juan Diego,Estudios,2026-09-15 19:13:27
48592018485,Laura Sofia,Estudios,2026-09-15 21:16:53
48592832256,Samuel David,Estudios,2026-09-16 23:15:32
48592832256,Samuel David,Estudios,2026-09-17 11:15:22
48592832256,Samuel David,Estudios,2026-09-17 13:15:41
48593069217,Paula Yisset Macias Monsalve,Estudios,2026-09-21 15:07:07
48594843688,Nicole Valentina Contreras Díaz,Estudios,2026-09-16 21:07:41
48594843688,Nicole Valentina Contreras Díaz,Estudios,2026-09-16 23:07:51
48594843688,Nicole Valentina Contreras Díaz,Estudios,2026-09-17 11:07:48
48594843688,Nicole Valentina Contreras Díaz,Estudios,2026-09-17 13:07:53
48594843688,Nicole Valentina Contreras Díaz,Estudios,2026-09-17 14:27:05
48598555063,Marvin,Estudios,2026-09-14 19:03:27
48598555063,Marvin,Estudios,2026-09-14 19:48:17
48599822415,Andy Alexander,Estudios,2026-09-15 21:10:01
48599992480,Juan Sebastian,Horarios,2026-09-16 15:22:27
48606200342,Danna Cecilia,Estudios,2026-09-16 23:11:33
48606200342,Danna Cecilia,Estudios,2026-09-17 11:11:27
48606200342,Danna Cecilia,Estudios,2026-09-17 13:11:40
48608366468,Juan Diego Sepulveda Melo,Estudios,2026-09-18 19:08:49
48609714454,Paula Lorena Galindo Romero,Estudios,2026-09-16 23:10:11
48609714454,Paula Lorena Galindo Romero,Estudios,2026-09-17 11:10:06
48609714454,Paula Lorena Galindo Romero,Estudios,2026-09-17 13:10:17
48609714454,Paula Lorena Galindo Romero,Estudios,2026-09-17 14:29:35
48611668035,Luz Dary Susa Rincón,Estudios,2026-09-17 17:05:55
48611668035,Luz Dary Susa Rincón,Estudios,2026-09-17 18:31:02
48611670561,Laura Camila Cardenas Granados,Estudios,2026-09-17 17:09:55
48611670561,Laura Camila Cardenas Granados,Estudios,2026-09-17 18:35:33
48612446489,Jefferson Hueso Rojas,Estudios,2026-09-17 17:13:49
48612446489,Jefferson Hueso Rojas,Estudios,2026-09-17 18:40:51
48613974708,Willman Steve,Estudios,2026-09-16 21:10:06
48617747882,Magnolia Rocio Lara Gualteros,Estudios,2026-09-18 21:07:51
48617857446,Brayan,Estudios,2026-09-16 23:13:57
48617857446,Brayan,Estudios,2026-09-17 11:13:50
48617857446,Brayan,Estudios,2026-09-17 13:14:05
48618362981,Karen Cristal Pérez Romero,Estudios,2026-09-18 17:07:30
48618365542,Luisa María Neme Pinzón,Estudios,2026-09-18 19:09:25
48619346483,Johan Minorta,Estudios,2026-09-21 19:08:42
48620121357,Juan David Bayona Torres,Estudios,2026-09-21 19:07:07
48620268349,Nathalia Estupiñan,Estudios,2026-09-21 17:07:04
48622499907,Nykol Juliana Bolaños Arias,Estudios,2026-09-16 19:05:59
48622499907,Nykol Juliana Bolaños Arias,Estudios,2026-09-16 21:06:00
48622499907,Nykol Juliana Bolaños Arias,Estudios,2026-09-16 23:06:06
48622499907,Nykol Juliana Bolaños Arias,Estudios,2026-09-17 11:06:04
48622499907,Nykol Juliana Bolaños Arias,Estudios,2026-09-17 13:06:11
48622499907,Nykol Juliana Bolaños Arias,Estudios,2026-09-17 14:24:00
48622520400,Daniel Chivara,Estudios,2026-09-17 17:11:15
48622520400,Daniel Chivara,Estudios,2026-09-17 18:38:04
48622520400,Daniel Chivara,Estudios,2026-09-18 19:01:15
48622632301,Ahileen,Horarios,2026-09-21 17:13:31
48622717038,Estiven,Horarios,2026-09-17 17:17:01
48623402756,Diego Fernando Jaramillo Reina,Estudios,2026-09-21 15:08:42
48626591522,Holmer Camilo Velez Gomez,Estudios,2026-09-17 21:08:46
48628515612,Edward Trujillo,Estudios,2026-09-18 23:09:00
48628665349,Evelyn Marín Orduña,Estudios,2026-09-18 17:01:58
48629110565,Sofia Sandoval Guzmán,Estudios,2026-09-17 18:43:31
48631145627,Andres Felipe Dueñas Martinez,Estudios,2026-09-18 19:10:00
48632233871,Luisa María Neme Pinzón,Estudios,2026-09-18 21:10:38
48632233871,Luisa María Neme Pinzón,Estudios,2026-09-18 23:08:29
48632673678,Marilyn Dayana Ramírez Cerquera,Estudios,2026-09-17 21:08:15
48632673678,Marilyn Dayana Ramírez Cerquera,Estudios,2026-09-18 17:01:21
48632673678,Marilyn Dayana Ramírez Cerquera,Estudios,2026-09-18 19:04:43
48632732753,Ahileen Daniela,Horarios,2026-09-21 13:09:40
48634694210,Magnolia Rocio Lara Gualteros,Estudios,2026-09-18 16:58:47
48638270393,Leidy Johana Paez Marquez,Estudios,2026-09-18 17:04:22
48638270393,Leidy Johana Paez Marquez,Estudios,2026-09-18 19:08:14
48639485707,Laura Sofia Roldán Hoyos,Estudios,2026-09-17 14:32:12
48639649369,Saray Tovar Murcia,Estudios,2026-09-17 18:46:03
48641277270,Ana Julieta Villa Durango,Estudios,2026-09-21 17:10:07
48650609968,Danna Castillo Rodriguez,Estudios,2026-09-21 17:08:44
48657127030,Lucia Del Carmen Tarapuez Taimal,Estudios,2026-09-22 17:12:57
48657279513,Nicolas Esteban Bello Martinez,Estudios,2026-09-22 15:53:57
48662151997,Nicoll Ruiz Quimbay,Estudios,2026-09-22 15:48:11
48663407142,Andres Castellanos Rodriguez,Estudios,2026-09-22 15:55:47
48664343177,Heidy Alejandra Sabogal Tamayo,Estudios,2026-09-22 19:11:13
48670387480,Carlos Andrés Robles Salas,Estudios,2026-09-22 17:07:14
48670391127,Paula Yisset Macias Monsalve,Estudios,2026-09-22 19:10:42
48673498750,Juan David Parra Tafur,Estudios,2026-09-22 21:09:49
48673809477,Jeison Yamid Pedraza Pedraza,Estudios,2026-09-22 21:11:27
48675387828,Sarita Saray Sierra,Estudios,2026-09-22 19:08:56
48681015643,Lucía Del Carmen Tarapuez Taimal,Estudios,2026-09-22 21:08:28
48681169737,Jhon Kener Sierra Daza,Estudios,2026-09-22 19:08:29
48681966347,Luisa María Neme Pinzón,Estudios,2026-09-23 15:08:30
48682400165,Angelyne Mariana Galán Ortiz,Estudios,2026-09-22 15:51:07
48684272932,Jhon Kener Sierra Daza,Estudios,2026-09-22 17:10:00
48691871321,Dayane Cuestas,Estudios,2026-09-24 21:11:08
48696830289,Sara Páramo Rojas,Estudios,2026-09-25 17:07:36
48696830289,Sara Páramo Rojas,Estudios,2026-09-25 19:07:24
48698878494,Darcy Tatiana Olmedo Espitia,Estudios,2026-09-25 21:08:22
48699325522,Angel Zuñiga,Estudios,2026-09-24 21:08:09
48699469979,Anyi Catalina Daza Carvajal,Estudios,2026-09-24 15:08:26
48699472669,Yeimy Tatiana Olaya Valbuena,Estudios,2026-09-24 17:07:27
48701153201,Maria Fernanda Cuadros Salamanca,Estudios,2026-09-23 15:30:45
48701203048,Pedro Pablo Martinez Aldana,Estudios,2026-09-23 23:11:40
48701350685,Marta Lucia Aparicio Guzman,Estudios,2026-09-23 17:06:12
48701376805,Joffre Enrique De La Hoz Camargo,Estudios,2026-09-24 19:05:14
48703890592,Aris Nelson Palacios Mosquera,Estudios,2026-09-24 15:14:21
48704026726,Sofia Montaño Guarnizo,Estudios,2026-09-23 17:09:17
48704051777,Deivid Santiago Torres Cano,Estudios,2026-09-24 21:10:59
48704341625,Laura Sofía Reyes Arevalo,Estudios,2026-09-23 23:08:54
48705968932,Alfredo Enrique Revollo Castañeda,Estudios,2026-09-25 17:13:17
48706487836,Sarita Saray Sierra,Estudios,2026-09-25 21:11:36
48714942825,Sharon Catalina Pinto Segura,Estudios,2026-09-24 15:11:31
48718879008,Danna Valentina Duarte Robayo,Estudios,2026-09-23 23:07:18
48720887322,Carlos Eduardo Rojas Medina,Estudios,2026-09-23 15:11:25
48740357702,Angel Zuñiga,Estudios,2026-09-24 19:05:08
48740686135,Karen Sofía Coral Ortiz,Estudios,2026-09-25 17:10:26
48744499107,Thalia Jazlin Monsalve Nieto,Estudios,2026-09-25 21:11:08"""

events = []
for line in events_raw.strip().split('\n'):
    parts = line.split(',')
    if len(parts) >= 4:
        events.append({
            'ticket': parts[0].strip(),
            'student': parts[1].strip(),
            'type': parts[2].strip(),
            'timestamp': parts[3].strip()
        })

print(f"Total events parsed: {len(events)}")

# Let's parse tickets table
tickets = []
lines = text.split('\n')
start_tickets = False
for line in lines:
    if line.startswith('Ticket,Estudiante,Tipo de Certificado,# de Envios'):
        start_tickets = True
        continue
    if start_tickets:
        if line.startswith('Ticket,Estudiante,Tipo de Certificado,Fecha y Hora'):
            break
        parts = line.split(',')
        if len(parts) >= 7:
            tickets.append({
                'ticket': parts[0].strip(),
                'student': parts[1].strip(),
                'type': parts[2].strip(),
                'sends': int(parts[3].strip()),
                'first_send': parts[4].strip(),
                'last_send': parts[5].strip(),
                'reprocessed': parts[6].strip()
            })

print(f"Total tickets parsed: {len(tickets)}")

# Analysis
# 1. Total emails: 414, Unique tickets: len(tickets)
# 2. Date breakdown
date_counts = defaultdict(int)
hour_counts = defaultdict(int)
for e in events:
    dt = datetime.strptime(e['timestamp'], '%Y-%m-%d %H:%M:%S')
    date_str = dt.strftime('%Y-%m-%d')
    date_counts[date_str] += 1
    hour_counts[dt.hour] += 1

# 3. Monthly / phase breakdown
# July: Testing phase
# Sept: "Production" phase
phase_counts = defaultdict(int)
for e in events:
    if e['timestamp'].startswith('2026-07'):
        phase_counts['Julio (Fase Pruebas/Alistamiento)'] += 1
    elif e['timestamp'].startswith('2026-09'):
        phase_counts['Septiembre (Fase "Producción" / En Ejecución)'] += 1
    else:
        phase_counts['Otro'] += 1

# 4. Reprocessing distribution
reprocess_dist = Counter([t['sends'] for t in tickets])

# 5. Top reprocessed
top_reprocessed = sorted(tickets, key=lambda x: x['sends'], reverse=True)[:15]

analysis_result = {
    'summary': {
        'total_emails': len(events),
        'unique_tickets': len(tickets),
        'reprocessed_tickets_count': sum(1 for t in tickets if t['sends'] > 1),
        'reprocessed_tickets_pct': round(sum(1 for t in tickets if t['sends'] > 1) / len(tickets) * 100, 2),
        'single_send_tickets': sum(1 for t in tickets if t['sends'] == 1),
        'single_send_pct': round(sum(1 for t in tickets if t['sends'] == 1) / len(tickets) * 100, 2),
        'estudios_tickets': sum(1 for t in tickets if t['type'] == 'Estudios'),
        'horarios_tickets': sum(1 for t in tickets if t['type'] == 'Horarios'),
        'max_sends': max(t['sends'] for t in tickets),
        'phase_counts': dict(phase_counts),
    },
    'date_distribution': sorted(dict(date_counts).items()),
    'hour_distribution': sorted(dict(hour_counts).items()),
    'reprocess_distribution': sorted(dict(reprocess_dist).items()),
    'top_reprocessed': top_reprocessed,
    'tickets': tickets,
    'events': events
}

with open('/Users/franciscomateus/Documents/DashboardUMB/processed_metrics.json', 'w') as f:
    json.dump(analysis_result, f, indent=2)

print("Analysis successfully written to processed_metrics.json")
