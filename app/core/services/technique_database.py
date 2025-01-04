from typing import Dict, List

class TechniqueDatabase:
    def get_technique_info(self, technique_name: str) -> Dict:
        techniques = {
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
                ],
                "resources": [
                    {
                        "title": "Social Skills Training Guide",
                        "url": "https://www.apa.org/topics/social-skills-training",
                        "type": "guide"
                    },
                    {
                        "title": "Practice Exercises",
                        "url": "https://www.verywellmind.com/social-skills-training-2584354",
                        "type": "exercises"
                    }
                ]
            },
            "Cognitive Behavioral Therapy (CBT)": {
                "description": "A therapy approach that helps identify and change negative thought patterns.",
                "steps": [
                    "Identify negative thoughts",
                    "Challenge cognitive distortions",
                    "Practice reframing thoughts",
                    "Track mood changes"
                ],
                "exercises": [
                    {
                        "name": "Thought Record",
                        "duration": "20 minutes",
                        "instructions": [
                            "Write down the situation",
                            "Note your automatic thoughts",
                            "Identify emotions",
                            "Find evidence for and against",
                            "Create balanced thought"
                        ]
                    }
                ],
                "resources": [
                    {
                        "title": "CBT Workbook",
                        "url": "https://www.psychologytools.com/self-help/cbt/",
                        "type": "workbook"
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
                ],
                "resources": [
                    {
                        "title": "Guided Meditations",
                        "url": "https://www.mindful.org/meditation/mindfulness-getting-started/",
                        "type": "audio"
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
                ],
                "resources": [
                    {
                        "title": "CBT Guide",
                        "url": "https://www.psychologytools.com/self-help/cbt/",
                        "type": "guide"
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
                ],
                "resources": [
                    {
                        "title": "Behavioral Activation Guide",
                        "url": "https://www.psychologytools.com/self-help/behavioral-activation/",
                        "type": "guide"
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
                ],
                "resources": [
                    {
                        "title": "Stress Management Guide",
                        "url": "https://www.apa.org/topics/stress/managing-stress",
                        "type": "guide"
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
                ],
                "resources": [
                    {
                        "title": "Therapy Guide",
                        "url": "https://www.apa.org/ptsd-guideline/patients-and-families/getting-professional-help",
                        "type": "guide"
                    }
                ]
            },
            "Gradual Exposure Therapy": {
                "description": "A therapeutic approach that gradually exposes you to anxiety-provoking situations in a controlled, safe environment to reduce fear and avoidance behaviors.",
                "steps": [
                    "Create a fear hierarchy (least to most anxiety-provoking)",
                    "Learn relaxation techniques for coping",
                    "Start with easiest exposure exercises",
                    "Progress gradually to more challenging situations",
                    "Practice regularly between sessions"
                ],
                "exercises": [
                    {
                        "name": "Situation Exposure Practice",
                        "duration": "30 minutes",
                        "instructions": [
                            "Choose a low-anxiety situation from your hierarchy",
                            "Use learned relaxation techniques before starting",
                            "Stay in the situation until anxiety reduces by 50%",
                            "Record your anxiety levels before, during, and after",
                            "Note what coping strategies worked best"
                        ]
                    }
                ],
                "resources": [
                    {
                        "title": "Understanding Exposure Therapy",
                        "url": "https://www.apa.org/ptsd-guideline/patients-and-families/exposure-therapy",
                        "type": "guide"
                    },
                    {
                        "title": "Exposure Therapy Workbook",
                        "url": "https://www.psychologytools.com/self-help/exposure-therapy/",
                        "type": "workbook"
                    }
                ]
            },
            "Cognitive Restructuring": {
                "description": "A technique to identify, challenge, and change negative thought patterns into more balanced and realistic ones.",
                "steps": [
                    "Identify negative automatic thoughts",
                    "Examine the evidence for and against",
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
                            "List your automatic negative thoughts",
                            "Rate your belief in each thought (0-100%)",
                            "Find evidence that supports and challenges each thought",
                            "Create a more balanced alternative thought"
                        ]
                    }
                ],
                "resources": [
                    {
                        "title": "Cognitive Restructuring Guide",
                        "url": "https://www.therapistaid.com/therapy-guide/cognitive-restructuring",
                        "type": "guide"
                    }
                ]
            },
            "Role-Playing Exercises": {
                "description": "Practice real-life situations in a safe, therapeutic environment to build confidence and develop new social skills.",
                "steps": [
                    "Identify challenging social situations",
                    "Plan specific scenarios to practice",
                    "Learn appropriate responses",
                    "Practice with feedback",
                    "Implement in real situations"
                ],
                "exercises": [
                    {
                        "name": "Scenario Practice",
                        "duration": "20 minutes",
                        "instructions": [
                            "Choose a specific social situation",
                            "Write out your ideal response",
                            "Practice the scenario with your therapist",
                            "Get feedback on your performance",
                            "Try alternative responses"
                        ]
                    }
                ],
                "resources": [
                    {
                        "title": "Role-Playing Techniques",
                        "url": "https://www.verywellmind.com/role-playing-social-anxiety-disorder-3024905",
                        "type": "guide"
                    }
                ]
            },
            "Relaxation Techniques": {
                "description": "Various methods to reduce physical and mental tension, helping manage anxiety and stress.",
                "steps": [
                    "Find a quiet, comfortable space",
                    "Learn different relaxation methods",
                    "Practice regularly",
                    "Monitor your tension levels",
                    "Use in stressful situations"
                ],
                "exercises": [
                    {
                        "name": "Progressive Muscle Relaxation",
                        "duration": "15 minutes",
                        "instructions": [
                            "Lie down or sit comfortably",
                            "Tense each muscle group for 5 seconds",
                            "Release and notice the relaxation",
                            "Move from toes to head",
                            "Focus on the contrast between tension and relaxation"
                        ]
                    }
                ],
                "resources": [
                    {
                        "title": "Relaxation Techniques Guide",
                        "url": "https://www.helpguide.org/articles/stress/relaxation-techniques-for-stress-relief.htm",
                        "type": "guide"
                    },
                    {
                        "title": "Guided Relaxation Audio",
                        "url": "https://www.calm.com/blog/breathing-exercises",
                        "type": "audio"
                    }
                ]
            },
            "Progressive Muscle Relaxation": {
                "description": "A deep relaxation technique that involves tensing and relaxing muscle groups systematically to reduce physical and mental tension.",
                "steps": [
                    "Find a quiet and comfortable space",
                    "Start with deep breathing exercises",
                    "Work through each muscle group",
                    "Hold tension for 5-10 seconds",
                    "Release and feel the relaxation"
                ],
                "exercises": [
                    {
                        "name": "Full Body Relaxation",
                        "duration": "20 minutes",
                        "instructions": [
                            "Start with your toes and feet",
                            "Move up through legs, torso, arms",
                            "End with neck and facial muscles",
                            "Notice the feeling of relaxation",
                            "Practice daily for best results"
                        ]
                    }
                ],
                "resources": [
                    {
                        "title": "PMR Guide",
                        "url": "https://www.uofmhealth.org/health-library/uz2225",
                        "type": "guide"
                    }
                ]
            },
            "Advanced Breathing Techniques": {
                "description": "Specialized breathing exercises to manage anxiety, reduce stress, and promote relaxation.",
                "steps": [
                    "Learn diaphragmatic breathing",
                    "Practice different breathing patterns",
                    "Use breathing as anxiety management",
                    "Incorporate mindfulness",
                    "Track effectiveness"
                ],
                "exercises": [
                    {
                        "name": "4-7-8 Breathing",
                        "duration": "10 minutes",
                        "instructions": [
                            "Inhale quietly through nose for 4 counts",
                            "Hold breath for 7 counts",
                            "Exhale completely through mouth for 8 counts",
                            "Repeat cycle 4 times",
                            "Practice 2-3 times daily"
                        ]
                    }
                ],
                "resources": [
                    {
                        "title": "Breathing Exercises Guide",
                        "url": "https://www.healthline.com/health/breathing-exercise",
                        "type": "guide"
                    }
                ]
            },
            "Mindfulness Meditation": {
                "description": "Present-moment awareness practice to reduce anxiety and improve emotional regulation.",
                "steps": [
                    "Find a quiet space",
                    "Set a timer for desired duration",
                    "Focus on your breath or body",
                    "Notice thoughts without judgment",
                    "Gently return focus when distracted"
                ],
                "exercises": [
                    {
                        "name": "Body Scan Meditation",
                        "duration": "15 minutes",
                        "instructions": [
                            "Lie down or sit comfortably",
                            "Bring attention to your body",
                            "Scan from feet to head",
                            "Notice sensations without judgment",
                            "Maintain gentle awareness"
                        ]
                    }
                ],
                "resources": [
                    {
                        "title": "Mindfulness Basics",
                        "url": "https://www.mindful.org/meditation/mindfulness-getting-started/",
                        "type": "guide"
                    }
                ]
            },
            "Behavioral Activation": {
                "description": "Structured approach to increase engagement in rewarding activities and combat depression.",
                "steps": [
                    "Monitor daily activities",
                    "Identify pleasurable activities",
                    "Schedule activities gradually",
                    "Track mood changes",
                    "Adjust based on progress"
                ],
                "exercises": [
                    {
                        "name": "Activity Planning",
                        "duration": "25 minutes",
                        "instructions": [
                            "List 5 activities you used to enjoy",
                            "Rate each for current difficulty (1-10)",
                            "Schedule one easier activity this week",
                            "Record your mood before and after",
                            "Celebrate completing the activity"
                        ]
                    }
                ],
                "resources": [
                    {
                        "title": "Behavioral Activation Guide",
                        "url": "https://www.psychologytools.com/self-help/behavioral-activation/",
                        "type": "workbook"
                    }
                ]
            },
            "Social Skills Training": {
                "description": "Structured practice to improve interpersonal communication and social confidence.",
                "steps": [
                    "Assess current social skills",
                    "Learn verbal/non-verbal communication",
                    "Practice in safe environment",
                    "Get feedback and adjust",
                    "Apply in real situations"
                ],
                "exercises": [
                    {
                        "name": "Conversation Practice",
                        "duration": "30 minutes",
                        "instructions": [
                            "Choose a conversation topic",
                            "Practice active listening",
                            "Use open-ended questions",
                            "Show appropriate non-verbal cues",
                            "Practice maintaining eye contact"
                        ]
                    }
                ],
                "resources": [
                    {
                        "title": "Social Skills Development",
                        "url": "https://www.verywellmind.com/social-skills-4157217",
                        "type": "guide"
                    }
                ]
            },
            "Interoceptive Exposure": {
                "description": "Technique to reduce fear of physical sensations associated with anxiety.",
                "steps": [
                    "Identify feared bodily sensations",
                    "Create hierarchy of exercises",
                    "Practice inducing sensations safely",
                    "Build tolerance gradually",
                    "Apply coping skills"
                ],
                "exercises": [
                    {
                        "name": "Sensation Exposure",
                        "duration": "20 minutes",
                        "instructions": [
                            "Choose a safe physical sensation",
                            "Induce it gradually",
                            "Rate anxiety level (0-10)",
                            "Stay with sensation until anxiety drops",
                            "Record your experience"
                        ]
                    }
                ],
                "resources": [
                    {
                        "title": "Understanding Interoceptive Exposure",
                        "url": "https://www.anxietycanada.com/articles/interoceptive-exposure/",
                        "type": "guide"
                    }
                ]
            }
        }
        return techniques.get(technique_name, {}) 