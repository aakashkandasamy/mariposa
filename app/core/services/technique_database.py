from typing import Dict, List

class TechniqueDatabase:
    def get_technique_info(self, technique_name: str) -> Dict:
        # Default structure for any unknown technique
        default_technique = {
            "description": f"A therapeutic technique focusing on {technique_name.lower()}.",
            "steps": [
                "Review the technique with your therapist",
                "Set specific goals for the session",
                "Practice the technique",
                "Get feedback and adjust",
                "Plan for home practice"
            ],
            "exercises": [
                {
                    "name": "Guided Practice",
                    "duration": "50 minutes",
                    "instructions": [
                        "Review previous progress",
                        "Set today's specific goals",
                        "Practice with guidance",
                        "Get feedback",
                        "Plan next steps"
                    ]
                }
            ]
        }

        techniques = {
            "Cognitive Behavioral Therapy (CBT)": {
                "description": "A structured therapeutic approach that helps identify and change negative thought patterns and behaviors.",
                "steps": [
                    "Identify negative thought patterns",
                    "Challenge cognitive distortions",
                    "Develop coping strategies",
                    "Practice behavioral changes",
                    "Monitor progress"
                ],
                "exercises": [
                    {
                        "name": "Thought Record Analysis",
                        "duration": "50 minutes",
                        "instructions": [
                            "Document triggering situations",
                            "Record automatic thoughts",
                            "Identify cognitive distortions",
                            "Create balanced responses",
                            "Practice new thinking patterns"
                        ]
                    }
                ]
            },
            "Social Skills Training": {
                "description": "A structured approach to improve social interactions and communication.",
                "steps": [
                    "Practice active listening",
                    "Learn to read body language",
                    "Practice conversation skills",
                    "Role-play social situations"
                ],
                "exercises": [
                    {
                        "name": "Active Listening Exercise",
                        "duration": "15 minutes",
                        "instructions": [
                            "Find a conversation partner",
                            "Listen without interrupting",
                            "Summarize what you heard",
                            "Ask relevant follow-up questions"
                        ]
                    },
                    {
                        "name": "Body Language Mirror",
                        "duration": "10 minutes",
                        "instructions": [
                            "Practice open posture",
                            "Maintain appropriate eye contact",
                            "Notice others' nonverbal cues"
                        ]
                    }
                ]
            },
            "Mindfulness Meditation": {
                "description": "Practices to stay present and aware of thoughts without judgment.",
                "steps": [
                    "Find a quiet space",
                    "Focus on breathing",
                    "Observe thoughts without attachment",
                    "Return focus when mind wanders"
                ],
                "exercises": [
                    {
                        "name": "5-Minute Breathing",
                        "duration": "5 minutes",
                        "instructions": [
                            "Sit comfortably",
                            "Close eyes or maintain soft gaze",
                            "Focus on natural breath",
                            "Count breaths from 1 to 10"
                        ]
                    }
                ]
            },
            "Regular CBT sessions": {
                "description": "Regular therapy sessions using Cognitive Behavioral Therapy techniques.",
                "steps": [
                    "Review previous week's progress",
                    "Identify current challenges",
                    "Apply CBT techniques",
                    "Set goals for next week"
                ],
                "exercises": [
                    {
                        "name": "Thought Challenging",
                        "duration": "30 minutes",
                        "instructions": [
                            "Identify a negative thought",
                            "Rate your belief in it (0-100%)",
                            "Find evidence for and against",
                            "Create a balanced perspective"
                        ]
                    }
                ]
            },
            "Behavioral Activation": {
                "description": "A structured approach to increase engagement in rewarding activities.",
                "steps": [
                    "Track daily activities",
                    "Rate activities for pleasure/mastery",
                    "Schedule enjoyable activities",
                    "Monitor mood changes"
                ],
                "exercises": [
                    {
                        "name": "Activity Scheduling",
                        "duration": "15 minutes",
                        "instructions": [
                            "List activities you used to enjoy",
                            "Rate each activity's difficulty (1-10)",
                            "Schedule one easy activity this week",
                            "Track your mood before and after"
                        ]
                    }
                ]
            },
            "Stress Management Techniques": {
                "description": "Various techniques to manage and reduce stress levels.",
                "steps": [
                    "Identify stress triggers",
                    "Learn relaxation techniques",
                    "Practice stress reduction",
                    "Monitor stress levels"
                ],
                "exercises": [
                    {
                        "name": "Progressive Muscle Relaxation",
                        "duration": "15 minutes",
                        "instructions": [
                            "Find a quiet space",
                            "Tense and relax each muscle group",
                            "Focus on the sensation",
                            "Progress from toes to head"
                        ]
                    }
                ]
            },
            "General therapy session": {
                "description": "A standard therapy session to discuss progress and challenges.",
                "steps": [
                    "Review recent experiences",
                    "Discuss any challenges",
                    "Apply learned techniques",
                    "Plan for the week ahead"
                ],
                "exercises": [
                    {
                        "name": "Weekly Review",
                        "duration": "50 minutes",
                        "instructions": [
                            "Reflect on the past week",
                            "Note any difficulties encountered",
                            "Celebrate progress made",
                            "Set goals for next week"
                        ]
                    }
                ]
            },
            "Gradual Exposure Therapy": {
                "description": "A therapeutic approach that gradually exposes you to anxiety-provoking situations in a controlled, safe environment to reduce fear and avoidance.",
                "steps": [
                    "Create a fear hierarchy",
                    "Start with least anxiety-provoking situations",
                    "Practice relaxation techniques",
                    "Gradually progress to more challenging situations",
                    "Track anxiety levels throughout exposure"
                ],
                "exercises": [
                    {
                        "name": "Situation Exposure Practice",
                        "duration": "30 minutes",
                        "instructions": [
                            "Choose a low-anxiety situation from your hierarchy",
                            "Rate anxiety before exposure (0-10)",
                            "Stay in the situation until anxiety reduces",
                            "Practice breathing exercises during exposure",
                            "Record your experience and progress"
                        ]
                    }
                ]
            },
            "Cognitive Restructuring": {
                "description": "A technique to identify and challenge negative thought patterns and replace them with more balanced, realistic thinking.",
                "steps": [
                    "Identify automatic negative thoughts",
                    "Examine evidence for and against",
                    "Consider alternative perspectives",
                    "Develop balanced thoughts",
                    "Practice new thinking patterns"
                ],
                "exercises": [
                    {
                        "name": "Thought Record Exercise",
                        "duration": "25 minutes",
                        "instructions": [
                            "Write down a troubling situation",
                            "Identify automatic negative thoughts",
                            "List evidence supporting and challenging thoughts",
                            "Create a balanced alternative thought",
                            "Rate belief in new perspective"
                        ]
                    }
                ]
            },
            "Role-Playing Exercises": {
                "description": "Practice real-life situations in a safe environment to build confidence and develop new social skills.",
                "steps": [
                    "Choose a challenging situation",
                    "Plan your response",
                    "Practice with feedback",
                    "Refine your approach",
                    "Gradually increase difficulty"
                ],
                "exercises": [
                    {
                        "name": "Social Scenario Practice",
                        "duration": "30 minutes",
                        "instructions": [
                            "Select a common social situation",
                            "Write out your ideal response",
                            "Practice with a therapist or trusted person",
                            "Get feedback on your approach",
                            "Try alternative responses"
                        ]
                    }
                ]
            },
            "Relaxation Techniques": {
                "description": "A collection of methods to reduce physical and mental tension through controlled breathing and muscle relaxation.",
                "steps": [
                    "Find a quiet, comfortable space",
                    "Focus on your breathing",
                    "Practice progressive muscle relaxation",
                    "Use guided imagery",
                    "Maintain regular practice"
                ],
                "exercises": [
                    {
                        "name": "Progressive Muscle Relaxation",
                        "duration": "20 minutes",
                        "instructions": [
                            "Lie down or sit comfortably",
                            "Tense and relax each muscle group",
                            "Focus on the contrast between tension and relaxation",
                            "Maintain slow, deep breathing",
                            "Notice the feeling of relaxation spreading"
                        ]
                    }
                ]
            },
            "Dialectical Behavior Therapy (DBT)": {
                "description": "A comprehensive treatment combining cognitive-behavioral techniques with mindfulness and acceptance strategies.",
                "steps": [
                    "Practice mindfulness skills",
                    "Develop emotion regulation",
                    "Improve interpersonal effectiveness",
                    "Build distress tolerance",
                    "Apply skills to daily life"
                ],
                "exercises": [
                    {
                        "name": "Emotion Regulation Practice",
                        "duration": "45 minutes",
                        "instructions": [
                            "Identify current emotions",
                            "Use mindfulness to observe feelings",
                            "Practice acceptance strategies",
                            "Apply DBT skills",
                            "Plan for skill practice"
                        ]
                    }
                ]
            }
        }

        # Return the specific technique if it exists, otherwise return the default
        return techniques.get(technique_name, default_technique) 