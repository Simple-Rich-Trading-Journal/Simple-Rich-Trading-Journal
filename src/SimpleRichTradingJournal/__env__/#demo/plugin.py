from secrets import randbelow

example_assets = {
    'TechNova Solutions': ['TechNova Solutions', 'Technology', 'TNVS', 'AAA', 'zzz', 0, None],
    'GlobalTech Innovations': ['GlobalTech Innovations', 'Technology', 'GLTCH', 'GGG', 'iii', 0, None],
    'NebulaElectronics Corporation': ['NebulaElectronics Corporation', 'Technology', 'NELEC', 'FFF', 'zzz', 0, None],
    'VirtuoNet Ventures': ['VirtuoNet Ventures', 'Technology', 'VNET', 'EEE', 'aaa', 0, None],
    'Luminary Systems International': ['Luminary Systems International', 'Technology', 'LUMSY', 'AAA', 'yyy', 0, None],
    'Axis Automation Group': ['Axis Automation Group', 'Technology', 'AXAUT', 'FFF', 'uuu', 1, 5],
    'QuantumCore Enterprises': ['QuantumCore Enterprises', 'Technology Intelligence', 'QNTCR', 'CCC', 'uuu', 0, None],
    'TerraRenew Corporation': ['TerraRenew Corporation', 'Technology Energy', 'TERRE', 'EEE', 'yyy', 0, None],
    'ApexStream Holdings': ['ApexStream Holdings', 'Technology', 'APEX', 'CCC', 'xxx', 0, 1],
    'SynergySolutions Inc.': ['SynergySolutions Inc.', 'Technology Integration', 'SYNSOL', 'GGG', 'uuu', 0, None],
    'Horizon Ventures Inc.': ['Horizon Ventures Inc.', 'Finance Capital', 'HORIZON', 'AAA', 'xxx', 0, None],
    'Nexus Dynamics Group': ['Nexus Dynamics Group', 'Finance Management', 'NXDYN', 'FFF', 'xxx', 1, None],
    'Infinity Financial Solutions': ['Infinity Financial Solutions', 'Finance', 'INFIN', 'EEE', 'uuu', 0, None],
    'StellarSpark Industries': ['StellarSpark Industries', 'Finance Banking', 'STSPK', 'FFF', 'xxx', 0, None],
    'FusionTech Capital': ['FusionTech Capital', 'Finance', 'FUSION', 'EEE', 'iii', 1, None],
    'Aurora Global Ventures': ['Aurora Global Ventures', 'Finance Equity', 'AURORA', 'GGG', 'uuu', 0, None],
    'EvolveSphere Capital': ['EvolveSphere Capital', 'Finance Management', 'EVOLVE', 'EEE', 'aaa', 1, None],
    'OmniWave Financials': ['OmniWave Financials', 'Finance Processing', 'OMWAV', 'EEE', 'aaa', 0, None],
    'Ecliptic Systems International': ['Ecliptic Systems International', 'Finance', 'ECLIPT', 'DDD', 'uuu', 1, None],
    'Vanguard Nexus Group': ['Vanguard Nexus Group', 'Finance Funds', 'VNGRD', 'DDD', 'aaa', 0, None],
    'Questify Pharmaceuticals': ['Questify Pharmaceuticals', 'Healthcare', 'QPHAR', 'BBB', 'zzz', 0, None],
    'MedTech Innovations': ['MedTech Innovations', 'Healthcare Devices', 'MEDIN', 'CCC', 'yyy', 0, None],
    'AlphaBio Corporation': ['AlphaBio Corporation', 'Healthcare', 'ALBIO', 'BBB', 'zzz', 0, None],
    'FutureCare Solutions': ['FutureCare Solutions', 'Healthcare Informatics', 'FUTCR', 'BBB', 'yyy', 0, None],
    'Celestial Health Ventures': ['Celestial Health Ventures', 'Healthcare', 'CELEH', 'DDD', 'xxx', 0, 3],
    'QuantumGenomics Inc.': ['QuantumGenomics Inc.', 'Healthcare', 'QGEN', 'DDD', 'uuu', 0, None],
    'InsightHealth Analytics': ['InsightHealth Analytics', 'Healthcare Analytics', 'INSHL', 'GGG', 'xxx', 0, None],
    'MedRobot Dynamics Inc.': ['MedRobot Dynamics Inc.', 'Healthcare Robotics', 'MDRBT', 'GGG', 'zzz', 0, None],
    'Empyrean Health Solutions': ['Empyrean Health Solutions', 'Healthcare Management', 'EMPYR', 'BBB', 'xxx', 0, None],
    'Transcend Wellness Holdings': ['Transcend Wellness Holdings', 'Healthcare', 'TRANWELL', 'AAA', 'zzz', 0, None],
    'ElysianTech Retail': ['ElysianTech Retail', 'E-Commerce', 'ELYTECH', 'BBB', 'yyy', 0, None],
    'Genesis Luxury Ventures': ['Genesis Luxury Ventures', 'Retail Goods', 'GENLV', 'EEE', 'uuu', 0, None],
    'InnovateMart Group': ['InnovateMart Group', 'Retail', 'INNOVM', 'AAA', 'yyy', 0, 7],
    'ZenithWorks International': ['ZenithWorks International', 'Retail Development', 'ZENWRK', 'CCC', 'aaa', 0, None],
    'PrimeLogistics Holdings': ['PrimeLogistics Holdings', 'Retail', 'PRIMLG', 'EEE', 'yyy', 0, None],
    'SynergyMarket Enterprises': ['SynergyMarket Enterprises', 'Retail Research', 'SYNMKT', 'BBB', 'iii', 0, None],
    'ApexZenith Retail': ['ApexZenith Retail', 'Retail Experience', 'APXZEN', 'CCC', 'uuu', 0, None],
    'QuantumQuest Ventures': ['QuantumQuest Ventures', 'Retail Marketing', 'QMQUEST', 'GGG', 'xxx', 0, None],
    'NebulaForge Solutions': ['NebulaForge Solutions', 'Retail Chain', 'NEBFOR', 'GGG', 'iii', 0, None],
    'VirtuosoTech Retail': ['VirtuosoTech Retail', 'Retail', 'VIRTCH', 'CCC', 'xxx', 1, None],
    'Luminex Motors Corporation': ['Luminex Motors Corporation', 'Automotive Vehicles', 'LUMX', 'GGG', 'zzz', 0, None],
    'HorizonForge Automotive': ['HorizonForge Automotive', 'Automotive', 'HORIZFRG', 'EEE', 'aaa', 1, None],
    'NexusDrive Innovations': ['NexusDrive Innovations', 'Automotive Vehicles', 'NXDRV', 'CCC', 'uuu', 0, None],
    'InfinityDrive Corporation': ['InfinityDrive Corporation', 'Automotive Systems', 'INFD', 'FFF', 'uuu', 0, None],
    'StellarDrive Ventures': ['StellarDrive Ventures', 'Automotive Technology', 'STDRV', 'DDD', 'zzz', 1, None],
    'FusionMotor Group': ['FusionMotor Group', 'Automotive Cells', 'FUSMOT', 'DDD', 'yyy', 0, None],
    'AuroraTech Automotive': ['AuroraTech Automotive', 'Automotive Design', 'AUTOTECH', 'FFF', 'uuu', 0, None],
    'EvolveSphere Mobility': ['EvolveSphere Mobility', 'Automotive', 'EVOLMOB', 'CCC', 'yyy', 0, None],
    'OmniNova Auto': ['OmniNova Auto', 'Mobility Automotive', 'OMNVA', 'EEE', 'yyy', 1, None],
    'EclipticPulse Automotive': ['EclipticPulse Automotive', 'Automotive', 'ECLIPAUTO', 'EEE', 'aaa', 0, None],
    'VanguardForge EdTech': ['VanguardForge EdTech', 'E-Learning', 'VNGDFG', 'DDD', 'uuu', 0, None],
    'QuestTech Education': ['QuestTech Education', 'Education', 'QSTTECH', 'DDD', 'aaa', 0, None],
    'ExcaliburSphere Learning': ['ExcaliburSphere Learning', 'Education Platforms', 'EXCSPL', 'FFF', 'aaa', 0, None],
    'AlphaNova Ed': ['AlphaNova Ed', 'Education Education', 'ALNOVA', 'FFF', 'aaa', 0, None],
    'FutureSphere EduTech': ['FutureSphere EduTech', 'Education Tutoring', 'FUTEDU', 'FFF', 'yyy', 0, None],
    'CelestialWorks EdTech': ['CelestialWorks EdTech', 'AI in Education', 'CELEDU', 'EEE', 'iii', 1, 4],
    'QuantumSphere Ed Ventures': ['QuantumSphere Ed Ventures', 'Education', 'QNTMED', 'AAA', 'xxx', 0, None],
    'InsightTech Ed Group': ['InsightTech Ed Group', 'Education Analytics for Schools', 'INSTED', 'CCC', 'iii', 0, None],
    'EndeavorForge Ed Innovations': ['EndeavorForge Ed Innovations', 'Education Support', 'ENDGFI', 'CCC', 'aaa', 1, None],
    'EmpyreanPulse Education': ['EmpyreanPulse Education', 'VR in Education', 'EMPYEDU', 'FFF', 'yyy', 0, None],
    'SolarNova Solutions': ['SolarNova Solutions', 'Energy', 'SOLRNOV', 'CCC', 'zzz', 0, None],
    'WindTech Ventures': ['WindTech Ventures', 'Energy', 'WNDTECH', 'CCC', 'iii', 0, None],
    'HydroGen Corporation': ['HydroGen Corporation', 'Energy Power', 'HYDROG', 'AAA', 'aaa', 0, 5],
    'BioFuel Innovations': ['BioFuel Innovations', 'Energy', 'BIOFUEL', 'AAA', 'zzz', 0, None],
    'Geothermal Dynamics Inc.': ['Geothermal Dynamics Inc.', 'Energy', 'GEOEN', 'AAA', 'aaa', 1, None],
    'TidalWave Energy Group': ['TidalWave Energy Group', 'Energy', 'TIDALE', 'BBB', 'yyy', 0, None],
    'FusionSolar Holdings': ['FusionSolar Holdings', 'Energy', 'FUSOLS', 'EEE', 'aaa', 0, 0],
    'CleanTech Solutions': ['CleanTech Solutions', 'Technology', 'CLEANT', 'EEE', 'uuu', 0, 0],
    'RenewablePower Corp.': ['RenewablePower Corp.', 'Power', 'RENPW', 'GGG', 'iii', 0, None],
    'ECOnergy Ventures': ['ECOnergy Ventures', 'Eco-friendly Energy', 'ECOENGY', 'GGG', 'yyy', 0, None],
    'AeroNova Technologies': ['AeroNova Technologies', 'Aerospace', 'AERONOV', 'BBB', 'uuu', 0, None],
    'SpaceTech Innovations': ['SpaceTech Innovations', 'Aerospace', 'SPTIN', 'AAA', 'iii', 0, 6],
    'AeroDynamics Corporation': ['AeroDynamics Corporation', 'Aerospace', 'AERODYN', 'FFF', 'xxx', 0, None],
    'AstroTech Ventures': ['AstroTech Ventures', 'Aerospace', 'ASTROV', 'GGG', 'yyy', 0, None],
    'OrbitalWorks International': ['OrbitalWorks International', 'Aerospace', 'ORBWORKS', 'GGG', 'yyy', 1, 7],
    'RocketForge Solutions': ['RocketForge Solutions', 'Aerospace', 'RCKTFOR', 'EEE', 'aaa', 0, None],
    'Lunar Dynamics Group': ['Lunar Dynamics Group', 'Aerospace', ' LUNDYN', 'AAA', 'xxx', 0, None],
    'StellarFlight Enterprises': ['StellarFlight Enterprises', 'Aerospace', 'STFLIGHT', 'BBB', 'aaa', 0, None],
    'CosmoTech Innovations': ['CosmoTech Innovations', 'Aerospace', 'COSMOTEC', 'CCC', 'iii', 0, None],
    'NebulaSpace Corporation': ['NebulaSpace Corporation', 'Aerospace', 'NEBUSPAC', 'DDD', 'xxx', 0, None],
    'Starlight Productions': ['Starlight Productions', 'Entertainment', 'STARPRO', 'FFF', 'iii', 0, None],
    'MusicNova Entertainment': ['MusicNova Entertainment', 'Entertainment', 'MUSICNOV', 'BBB', 'iii', 1, None],
    'GameTech Studios': ['GameTech Studios', 'Entertainment', 'GAMETEC', 'GGG', 'yyy', 1, 1],
    'VirtualWorld Ventures': ['VirtualWorld Ventures', 'Virtual Reality', 'VRWORLD', 'BBB', 'xxx', 0, None],
    'ComicSphere Enterprises': ['ComicSphere Enterprises', 'Entertainment', 'COMSPH', 'EEE', 'yyy', 0, None],
    'StageCraft Innovations': ['StageCraft Innovations', 'Entertainment', 'STGCRFT', 'CCC', 'iii', 0, None],
    'SportsEdge Holdings': ['SportsEdge Holdings', 'Entertainment', 'SPORTED', 'AAA', 'iii', 0, None],
    'MediaFusion Corporation': ['MediaFusion Corporation', 'Entertainment', 'MDFUSN', 'BBB', 'yyy', 0, None],
    'ArtTech Creations': ['ArtTech Creations', 'Entertainment', 'ARTTECH', 'BBB', 'uuu', 1, None],
    'NoveltyWorks International': ['NoveltyWorks International', 'Novelty Items', 'NOVELTYW', 'AAA', 'xxx', 0, None],
    'DreamScape Resorts': ['DreamScape Resorts', 'Hospitality', 'DRMSRC', 'DDD', 'xxx', 0, 9],
    'StellarStay Hotels': ['StellarStay Hotels', 'Hospitality', 'STYHOT', 'BBB', 'xxx', 0, None],
    'FoodFusion Hospitality': ['FoodFusion Hospitality', 'Hospitality', 'FDFUSN', 'AAA', 'zzz', 0, None],
    'AdventureWorks Travel': ['AdventureWorks Travel', 'Travel Agencies', 'ADVTRVL', 'DDD', 'xxx', 0, None],
    'Blissful Retreats': ['Blissful Retreats', 'Hospitality', 'BLISSRT', 'FFF', 'zzz', 0, None],
    'EventElevate Enterprises': ['EventElevate Enterprises', 'Event Planning', 'EVTELEV', 'DDD', 'zzz', 0, None],
    'SerenityStay Inns': ['SerenityStay Inns', 'Hospitality', 'SRNSTAY', 'BBB', 'xxx', 0, None],
    'ExoticEscape Travel Group': ['ExoticEscape Travel Group', 'Luxury Travel', 'EXTESC', 'EEE', 'uuu', 0, 5],
    'Harmony Heights Resorts': ['Harmony Heights Resorts', 'Eco Resorts', 'HARMRES', 'AAA', 'uuu', 0, None],
    'TranquilTides Retreats': ['TranquilTides Retreats', 'Beach Resorts', 'TRQTIDE', 'GGG', 'xxx', 0, 9],
}


def _randint(a, b):
    c = b - a
    return randbelow(c + 1) + a


def _randrate():
    i = _randint(0, 8)
    if i < 3:
        return _randint(3_00, 8_00) / 100_00
    if i < 6:
        return _randint(2_70, 3_60) / 100_00
    return _randint(30, 4_90) / 100_00


def course_call(row_data: dict, manual_take_amount: bool) -> bool:
    if not manual_take_amount:
        c = row_data.get("TakeCourse") or row_data["InvestCourse"]
        if c:
            if _randint(0, 1):
                c *= (1 + _randrate())
            else:
                c *= (1 - _randrate())
            row_data["TakeCourse"] = c
            row_data["TakeAmount"] = c * row_data["n"]
            return True
    else:
        return False


def symbol_call(update_data: dict) -> None:
    if asset := example_assets.get(update_data.get("value")):
        update_data["data"] |= {"Sector": asset[1], "Symbol": asset[2], "Type": asset[3], "Category": asset[4], "Short": bool(asset[5]), "Rating": asset[6]}
