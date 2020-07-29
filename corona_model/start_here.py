import model_framework
import platform


def main():
    """intialize and run the model, for indepth detail about the config or how to run the code, go to the github page for this code"""    
    modelConfig = {
        "Agents" : {
            "PossibleStates":{
                "neutral" : ["susceptible", "exposed"],
                "infected" : ["infected Asymptomatic", "infected Asymptomatic Fixed", "infected Symptomatic Mild", "infected Symptomatic Severe"],  
                "recovered" : ["quarantined", "recovered"],
                "debugAndGraphingPurpose": ["falsePositive"],
                },
            "ExtraParameters":[
                        "agentId","path", "destination", "currLocation",
                        "statePersistance","lastUpdate", "personality", 
                        "arrivalTime", "schedule",  "gathering",
                        # "travelTime", "officeAttendee",
                ], # travelTime and officeAttendee will be commented out
            "ExtraZipParameters": [("motion", "stationary"), ("infected", False), ("compliance", False)],
            "booleanAssignment":[ ("gathering", 0.5)], # ("officeAttendee", 0),
            
        },
        "Rooms" : {
            "ExtraParameters": ["roomId","agentsInside","oddCap", "evenCap", "classname", "infectedNumber", "hubCount"],
        },
        "Buildings" : {
            "ExtraParameters": ["buildingId","roomsInside"],
        },
        "Infection" : {
            "baseP" : 1.15,
            "SeedNumber" : 10,
            "SeedState" : "exposed",
            "Contribution" : {
                "infected Asymptomatic":0.5,
                "infected Asymptomatic Fixed":0.5,
                "infected Symptomatic Mild":1,
                "infected Symptomatic Severe":1,
            },
            # INFECTION STATE
            "TransitionTime" : {
                "susceptible" : -1, # never, unless acted on
                "exposed" : 2*24, # 2 days
                "infected Asymptomatic" : 2*24, # 2 days
                "infected Asymptomatic Fixed" : 10*24, # 10 days
                "infected Symptomatic Mild" : 10*24,# 10 Days
                "infected Symptomatic Severe" : 10*24, # 10 days
                "recovered" : -1, # never
                "quarantined" : 24*14, # 2 weeks 
            },
            # INFECTION TRANSITION PROBABILITY
            "TransitionProbability" : {
                "susceptible" : [("exposed", 1)],
                "exposed" : [("infected Asymptomatic", 0.85), ("infected Asymptomatic Fixed", 1)],
                "infected Asymptomatic Fixed": [("recovered", 1)],
                "infected Asymptomatic": [("infected Symptomatic Mild", 0.5), ("infected Symptomatic Severe", 1)],
                "infected Symptomatic Mild": [("recovered", 1)],
                "infected Symptomatic Severe": [("recovered", 1)],
                "quarantined":[("susceptible", 1)],
                "recovered":[("susceptible", 0.5), ("recovered", 1)],
            },
        },
        "World" : {
            "UnitTime" : "Hours",
            # by having the supposed days to be simulated, 
            # we can allocate the required space beforehand to speedup data storing
            "InferedSimulatedDays":100,
            # put the name(s) of intervention(s) to be turned on 
            "TurnedOnInterventions":[],# ["HybridClasses", "ClosingBuildings", "Quarantine", "FaceMasks"], 
            "permittedAction": [],#["walkin"],
            "transitName": "transit_space_hub",
            "offCampusInfectionProbability":0.125/880,
            "massInfectionRatio":0.10,
            "complianceRatio": 0,
            "stateCounterInterval": 5,
            "socialInteraction": 0.15,
            "LazySunday": True,
            "LargeGathering": True,
        },
       
        # interventions
        "FaceMasks" : {
            "MaskInfectivity" : 0.5,
            "MaskBlock":0.75,
            "NonCompliantLeaf": ["dorm", "dining", "faculty_dining_hall"],
            "CompliantHub" : ["dorm", "dining"],
            "NonCompliantBuilding" : ["social", "largeGathering"],
        },
        "Quarantine" : {
            # this dictates if we randomly sample the population or cycle through Batches
            "RandomSampling": False,
            # for random sampling from the agent population
            "SamplingProbability" : 0,
            "SampleSizeForTesting":50,
            "ResultLatency":24,
            "walkinProbability" : {
                "infected Symptomatic Mild": 0.7, 
                "infected Symptomatic Severe": 0.95,
                },
            "BatchSize" : 400,
            "ShowingUpForScreening": 1,
            "offset": 9, # start at 9AM
            "checkupFrequency": 24*1,
            "falsePositive":0.001,
            "falseNegative":0#0.03,
        },
        "ClosingBuildings": {
            "ClosedBuildingType" : ["gym", "library"],
            "ClosedButKeepHubOpened" : [],
            "GoingHomeP": 0.5,
        },
        "HybridClass":{
            "RemoteStudentCount": 1000,
            "RemoteFacultyCount": 180,
            "RemovedDoubleCount": 0,
            "OffCampusCount": 500,
            "TurnOffLargeGathering": True,
        },
        "LessSocializing":{
            "SocializingProbability":0.5
        }

    }
    """
    notes:
    in the table dining hall core is 600*10
    in section 3.1, under faculty: there are 380 faculty and it sums to 2380
    in the base model table, there is T{sub}Ie0 and T{sub}Ie1 which is the # of days infected and bed-ridden.  In the base model, I have it so all symptomatic Severe are bed-ridden after 5 days.
    is there a case where the severe agents are not bed-ridden?
    """
    # you can control for multiple interventions by adding a case:
    #  [(modified attr1, newVal), (modified attr2, newVal), ...]

    # simulation name --> simulation controlled variable(s)
    # dont use . or - in the simulation name because the names are used to save images, or any symbols below
    """
        < (less than)
        > (greater than)
        : (colon - sometimes works, but is actually NTFS Alternate Data Streams)
        " (double quote)
        / (forward slash)
        \ (backslash)
        | (vertical bar or pipe)
        ? (question mark)
        * (asterisk)
    """
    ControlledExperiment = {
        "baseModel":{}, # no changes
        "Minimal": {
            "World": [
                ("TurnedOnInterventions", ["FaceMasks", "Quarantine"]),
                ("ComplianceRatio", 0.5),
                ],
            "Quarantine": [
                ("ResultLatency", 3*24), 
                ("SampleSizeForTesting", 100),
                ( "ShowingUpForScreening", 0.8),
                ],
        }, 
        "Moderate": {
            "World": [
                ("TurnedOnInterventions", ["FaceMasks", "Quarantine", "ClosingBuildings"]),
                ("ComplianceRatio", 0.5)
            ],
            "Quarantine": [
                ("ResultLatency", 3*24), 
                ("SampleSizeForTesting", 250),
               
                ("BatchSize", 250),
                ( "ShowingUpForScreening", 0.8),
                ],
            "ClosingBuildings": [
                ("ClosedBuildingType", ["gym", "library"]),
                ("GoingHomeP", 0.5),
            ]
        },    
        "Moderate+StrongerFacemask": {
            "World": [
                ("TurnedOnInterventions", ["FaceMasks", "Quarantine", "ClosingBuildings"]),
                ("ComplianceRatio", 1),
            ],
            "Quarantine": [
                ("ResultLatency", 3*24), 
                ("SampleSizeForTesting", 250),
                ("BatchSize", 250),
                ( "ShowingUpForScreening", 0.8),
                ],
            "ClosingBuildings": [
                ("ClosedBuildingType", ["gym", "library"]),
                ("GoingHomeP", 0.5),
            ]
        },
        "Moderate+DiningHallClosure": { # skip #####################
            "World": [
                ("TurnedOnInterventions", ["FaceMasks", "Quarantine",  "ClosingBuildings"]),
                ("ComplianceRatio", 0.5)
            ],
            "Quarantine": [
                ("ResultLatency", 3*24), 
                ("SampleSizeForTesting", 250),
                ("BatchSize", 250),
                ( "ShowingUpForScreening", 0.8),
                ],
            "ClosingBuildings": [
                ("ClosedBuildingType", ["gym", "library", "dining", "faculty_dining_room"]),
                ("ClosedButKeepHubOpened", []),
                ("GoingHomeP", 0.5),
            ]
        },
        "Moderate+LessSocializing": {
            "World": [
                ("TurnedOnInterventions", ["FaceMasks", "Quarantine","ClosingBuildings", "LessSocial"]),
                ("ComplianceRatio", 0.5),
                ("LargeGathering", False),
            ],
            "Quarantine": [
                ("ResultLatency", 3*24), 
                ("SampleSizeForTesting", 250),
                ("BatchSize", 250),
                ( "ShowingUpForScreening", 0.8),
                ],
            "ClosingBuildings": [
                ("ClosedBuildingType", ["gym", "library"]),
                ("GoingHomeP", 1),
            ]
        },  
        "Moderate+MediumDeden": {
            "World": [
                ("TurnedOnInterventions", ["FaceMasks", "Quarantine", "ClosingBuildings","HybridClasses"]),
                ("ComplianceRatio", 0.5)
            ],
            "Quarantine": [
                ("ResultLatency", 3*24), 
                ("SampleSizeForTesting", 250),
                ("BatchSize", 250),
                ( "ShowingUpForScreening", 0.8),
                ],
            "ClosingBuildings": [
                ("ClosedBuildingType", ["gym", "library"]),
                ("GoingHomeP", 0.5),
            ],
            "HybridClass":[
                ("RemoteStudentCount", 750),
                ("RemoteFacultyCount", 100),
                ("OffCampusCount", 250),
                ("RemovedDoubleCount", 250),
                ("TurnOffLargeGathering", True),
            ],
        }, 
        "Moderate+MediumDeden+LessSocial": {
            "World": [
                ("TurnedOnInterventions", ["FaceMasks", "Quarantine", "ClosingBuildings","HybridClasses", "LessSocial"]),
                ("ComplianceRatio", 0.5)
            ],
            "Quarantine": [
                ("ResultLatency", 3*24), 
                ("SampleSizeForTesting", 250),
                ("BatchSize", 250),
                ( "ShowingUpForScreening", 0.8),
                ],
            "ClosingBuildings": [
                ("ClosedBuildingType", ["gym", "library"]),
                ("GoingHomeP", 0.5),
            ],
            "HybridClass":[
                ("RemoteStudentCount", 750),
                ("RemoteFacultyCount", 100),
                ("OffCampusCount", 250),
                ("RemovedDoubleCount", 250),
                ("TurnOffLargeGathering", True),
            ]
      
        },
        "Moderate+HighDeden": {
            "World": [
                ("TurnedOnInterventions", ["FaceMasks", "Quarantine", "ClosingBuildings","HybridClasses"]),
                ("ComplianceRatio", 0.5)
            ],
            "Quarantine": [
                ("ResultLatency", 3*24), 
                ("SampleSizeForTesting", 250),
                ("BatchSize", 250),
                ( "ShowingUpForScreening", 0.8),
                ],
            "ClosingBuildings": [
                ("ClosedBuildingType", ["gym", "library"]),
                ("GoingHomeP", 0.5),
            ],
            # no chnage to "HybridClass"
        },
         

        "Maximal": {
            "World": [
                ("TurnedOnInterventions", ["FaceMasks", "Quarantine", "ClosingBuildings","HybridClasses", "LessSocial"]),
                ("ComplianceRatio", 1),
                
            ],
            "Infection":[
                ("SeedNumber", 5),
            ],
            "Quarantine": [
                ("ResultLatency", 1*24), 
                ("SampleSizeForTesting", 500),
                ("BatchSize", 500),
                ( "ShowingUpForScreening", 1),
                ],
            "ClosingBuildings": [
                ("ClosedBuildingType", ["gym", "library", "office", "dining", "faculty_dining_room"]),
                ("ClosedButKeepHubOpened", ["dining"]),
                ("GoingHomeP", 1),
            ],
            "HybridClass":[
                ("RemoteStudentCount", 1000),
                ("RemovedDoubleCount", 525),
                ("RemoteFacultyCount", 180),
                ("OffCampusCount", 500),
                ("TurnOffLargeGathering", True),
            ],
        },
    }
    R0_controls = {
        "World": [()]
    }
    R0Dict = dict()
    simulationGeneration = "1"
    osName = platform.system()
    files = "images\\" if osName.lower() == "windows" else "images/"
    for index, (modelName, modelControl) in enumerate(ControlledExperiment.items()):
        configCopy = dict(modelConfig)
        print("*"*20)
        print(f"started working on initializing the simualtion for {modelName}")
        for categoryKey, listOfControls in modelControl.items():
            for (specificKey, specificValue) in listOfControls:
                configCopy[categoryKey][specificKey] = specificValue
        R0Count = 10 if index < 1 else 1
        multiCounts = 1
        if index in [0, 1]:
            typeName = "p_" + str(configCopy["Infection"]["baseP"]) + "_"
            modelName=files+typeName+modelName+"_"+str(simulationGeneration)
            #model_framework.simpleCheck(configCopy, days=100, visuals=True, debug=False, modelName=modelName)
            #model_framework.multiSimulation(multiCounts, configCopy, days=100, debug=False, modelName=modelName) 
            R0Dict[modelName] = model_framework.R0_simulation(modelConfig, R0_controls,R0Count, debug=True, visual=False)
           
            
    print(R0Dict.items())
if __name__ == "__main__":
    main()