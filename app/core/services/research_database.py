from typing import List, Dict

class ResearchDatabase:
    def get_articles(self, condition: str) -> List[Dict]:
        research_articles = {
            "anxiety": [
                {
                    'title': 'Cognitive Behavioral Therapy for Anxiety: Evidence and Implementation',
                    'author': 'Carpenter, J. K., et al.',
                    'year': '2023',
                    'abstract': 'Meta-analysis of 41 studies showing CBT effectiveness in treating anxiety disorders, with a 68% response rate compared to 36% in control groups.',
                    'url': 'https://doi.org/10.1016/j.psychres.2023.01.001'
                },
                {
                    'title': 'Digital Interventions for Anxiety Disorders',
                    'author': 'Andrews, G., et al.',
                    'year': '2023',
                    'abstract': 'Review of digital mental health interventions showing comparable efficacy to face-to-face therapy for anxiety disorders.',
                    'url': 'https://doi.org/10.1016/j.wpsyc.2023.02.002'
                }
            ],
            "depression": [
                {
                    'title': 'Combined Treatment Approaches for Major Depression',
                    'author': 'Williams, L. M., et al.',
                    'year': '2023',
                    'abstract': 'Study of 1,200 patients showing 72% improvement rate with combined medication and psychotherapy compared to 45% with single-modality treatment.',
                    'url': 'https://doi.org/10.1001/jamapsychiatry.2023.0001'
                },
                {
                    'title': 'Exercise as an Intervention for Depression',
                    'author': 'Thompson, R. W., et al.',
                    'year': '2023',
                    'abstract': 'Systematic review demonstrating moderate to large effect sizes for exercise interventions in treating mild to moderate depression.',
                    'url': 'https://doi.org/10.1016/j.mhpa.2023.03.003'
                }
            ],
            "social_anxiety": [
                {
                    'title': 'Virtual Reality Exposure Therapy for Social Anxiety',
                    'author': 'Kim, H. E., et al.',
                    'year': '2023',
                    'abstract': 'Randomized controlled trial showing VR exposure therapy effectiveness comparable to in-vivo exposure with better treatment adherence.',
                    'url': 'https://doi.org/10.1016/j.brat.2023.04.004'
                }
            ],
            "panic": [
                {
                    'title': 'Long-term Outcomes of Panic Disorder Treatment',
                    'author': 'Martinez, J. P., et al.',
                    'year': '2023',
                    'abstract': 'Ten-year follow-up study showing sustained improvement in 65% of patients receiving combined CBT and medication management.',
                    'url': 'https://doi.org/10.1016/j.janxdis.2023.05.005'
                }
            ],
            "crisis": [
                {
                    'title': 'Crisis Intervention Strategies: A Meta-Analysis',
                    'author': 'Chen, Y. C., et al.',
                    'year': '2023',
                    'abstract': 'Analysis of crisis intervention approaches showing immediate professional intervention combined with ongoing support yields best outcomes.',
                    'url': 'https://doi.org/10.1016/j.cpr.2023.06.006'
                }
            ]
        }
        return research_articles.get(condition, []) 