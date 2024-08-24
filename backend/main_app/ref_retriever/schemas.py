from pydantic import BaseModel, Field
from typing import List

class TextInput(BaseModel):
    text: str = Field(
        example="""
            In this context, several approaches for cross-modal retrieval between visual data and
            text description have been proposed, such as [6–11], to name but a few. Many of them are
            image-text retrieval methods that make use of a projection of the image features and the
            text features into the same space (visual, textual or a joint space) so that the retrieval is then
            performed by searching in this latent space (e.g., [12–14]). Other approaches are referred as
            video-text retrieval methods as they learn embeddings of video and text in the same space
            by using different multi-modal features (like visual cues, video dynamics, audio inputs,
            and text) [8,9,15–18]. For example, Ref. [8] simultaneously utilizes multi-modal features
            to learn two joint video-text embedding networks: one learns a joint space between text
            features and visual appearance features, the other learns a joint space between text features
            and a combination of activity and audio features.
            Many attempts for developing effective visual retrieval systems have been done
            since the 1990s, such as content-based querying system for video databases [19–21] or
            the query by image content system presented in [22]. Many video retrieval systems are
            designed in order to support complex human generated queries that may include but are
            not limited to keywords or natural language sentences. Most of them are interactive tools
            where the users can dynamically refine their queries in order to better specify their search
            intent during the search process. The VBS contest provides a live and fair performance
            assessment of interactive video retrieval systems and therefore in recent years has become
            a reference point for comparing state-of-the-art video search tools. During the competition,
            the participants have to perform various KIS and AVS tasks in a limited amount of time
            (generally within 5–8 min for each task). To evaluate the interactive search performance
            of each video retrieval system, several search sessions are performed by involving both
            expert and novice users. Expert users are the developers of the in race retrieval system or
            people that already know and use the system before the competition. Novices are users
            who interact with the search system for the first time during the competition.
            Several video retrieval systems participated at the VBS in the last years [1,3,23,24].
        """
    )