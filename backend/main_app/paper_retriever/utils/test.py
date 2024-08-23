import re

references = """
References
1. Radford A et al (2021) Learning transferable visual models from
natural language supervision. In: Meila M, Zhang T (eds.) Proceed-ings of the 38th international conference on machine learning, vol139 of Proceedings of machine learning research, pp 8748–8763(PMLR). https://proceedings.mlr.press/v139/radford21a.html
2. Lokoˇ c J et al (2023) Interactive video retrieval in the age of effective
 joint embedding deep models: lessons from the 11th VBS.Multimed Syst. https://doi.org/10.1007/s00530-023-01143-5
3. Heller S et al (2022) Interactive video retrieval evaluation at a
distance: comparing sixteen interactive video search systems in aremote setting at the 10th video browser showdown. Int J MultimedInf Retr 11:1–18. https://doi.org/10.1007/s13735-021-00225-2
4. Lokoˇ c J et al (2021) Is the reign of interactive search eternal?
Findings from the video browser showdown 2020. ACM TransMultimed Comput Commun Appl (TOMM). https://doi.org/10.
1145/3445031
5. Gurrin C et al (2023) Introduction to the sixth annual lifelog
search challenge, LSC’23. In: Kompatsiaris IY , et al (eds.) Proceed-ings international conference on multimedia retrieval (ICMR’23)(ACM, Thessaloniki, Greece)
6. Awad G et al (2022) An overview on the evaluated video retrieval
tasks at trecvid 2022. In: Awad G (ed.) Proceedings of TRECVID2022 (NIST, USA)
7. Constantin MG, Hicks S, Larson M, Nguyen N-T (2020) MediaEval
 multimedia evaluation benchmark: tenth anniversary andcounting. ACM SIGMM Rec 12:1–1
8. Lokoˇ c J et al (2022) A task category space for user-centric comparative
 multimedia search evaluations. In: Þór Jónsson B, et al (eds.)International conference on multimedia modeling
9. Lokoˇ c J, Bailer W, Schoeffmann K, Münzer B, Awad G (2018)
On influential trends in interactive video retrieval: video browsershowdown 2015–2017. IEEE Trans Multimed 20:3361–3376
10. Gurrin C et al (2022) Introduction to the fifth annual lifelog search
challenge, LSC’22. In: Oria V , et al (eds.) ICMR’22: internationalconference on multimedia retrieval, Newark, June 27–30, 2022, pp685–687 (ACM). https://doi.org/10.1145/3512527.3531439
11. Tran L et al (2023) Comparing interactive retrieval approaches at
the lifelog search challenge 2021. IEEE Access 11:30982–30995.
https://doi.org/10.1109/ACCESS.2023.3248284
12. Rossetto L et al (2021) On the user-centric comparative remote
evaluation of interactive video search systems. IEEE MultiMed.https://doi.org/10.1109/MMUL.2021.3066779
13. Hezel N, Schall K, Jung K, Barthel KU (2022) Efficient search
and browsing of large-scale video collections with vibro. In: ÞórJónsson B, et al (eds.) MultiMedia modeling. Springer, Cham, pp487–492
14. Lokoˇ c J, Mejzlík F, Souˇ cek T, Dokoupil P, Peška L (2022) Video
search with context-aware ranker and relevance feedback. In: ÞórJónsson, B. et al (eds.) MultiMedia modeling. Springer Cham, pp505–510
15. Amato G et al (2022) Visione at video browser showdown 2022. In:
Þór Jónsson B, et al (eds.) MultiMedia modeling. Springer, Cham,pp 543–54816. He K, Zhang X, Ren S, Sun J (2016) Deep residual learning for
image recognition. In: 2016 IEEE conference on computer visionand pattern recognition (CVPR)
17. Philbin J, Chum O, Isard M, Sivic J, Zisserman A (2007) Object
retrieval with large vocabularies and fast spatial matching. In: 2007IEEE conference on computer vision and pattern recognition (IEEEComputer Society)
18. Dosovitskiy A et al (2020) An image is worth 16 ×16 words:
transformers for image recognition at scale. In: CoRR
19. Messina N, Falchi F, Esuli A, Amato G (2021) Transformer reasoning
 network for image–text matching and retrieval. In: 202025th International conference on pattern recognition (ICPR), pp5222–5229 (IEEE)
20. Fang H, Xiong P, Xu L, Chen Y (2021) Clip2video: Mastering
 video-text retrieval via image clip. arXiv preprintarXiv:2106.11097
21. Liu Z et al (2021) Swin transformer: Hierarchical vision transformer
 using shifted windows. arXiv preprint arXiv:2103.14030
22. Russakovsky O et al (2015) ImageNet large scale visual recognition
challenge. Int J Comput Vis 115:211
23. Kim S, Kim D, Cho M, Kwak S (2020) Proxy anchor loss for deep
metric learning. In: IEEE/CVF conference on computer vision and
pattern recognition (CVPR)
24. Cox I, Miller M, Omohundro S, Yianilos P (1996) Pichunter:
Bayesian relevance feedback for image retrieval. In: Internationalconference on pattern recognition, vol 3, pp 361–369 (IEEE).https://doi.org/10.1109/ICPR.1996.546971
25. Lokoc J, Peska L (2023) A study of a cross-modal interactive
search tool using CLIP and temporal fusion. Dang-Nguyen Det al (eds.) MultiMedia modeling—29th international conference,MMM 2023, Bergen, Norway, January 9–12, 2023, Proceedings,Part I, V ol. 13833 of Lecture Notes in Computer Science. Springer,pp 397–408. https://doi.org/10.1007/978-3-031-27077-2_31
26. Revaud J, Almazan J, Rezende R, de Souza C (2019) Learning
with average precision: training image retrieval with a listwise loss.In: International conference on computer vision, pp 5106–5115(IEEE). https://doi.org/10.1109/ICCV .2019.00521
27. Zhang H, Wang Y , Dayoub F, Sunderhauf N (2021) VarifocalNet:
an IoU-aware dense object detector. In: 2021 IEEE/CVF confer-ence on computer vision and pattern recognition (CVPR) (IEEE)
28. He K, Gkioxari G, Dollár P, Girshick R (2017) Mask R-CNN.
In: Proceedings of the IEEE international conference on computervision, pp 2961–2969
29. Girshick R (2015) Fast R-CNN. In: Proceedings of the IEEE international
 conference on computer vision, pp 1440–1448
30. Van De Weijer J, Schmid C, Verbeek J, Larlus D (2009) Learning
color names for real-world applications. IEEE Trans Image Process
18:1512–1523. https://doi.org/10.1109/TIP.2009.2019809
31. Benavente R, Vanrell M, Baldrich R (2008) Parametric fuzzy sets
for automatic color naming. JOSA A 25:2582–2593. https://doi.
org/10.1364/JOSAA.25.002582
32. Kohonen T (1982) Self-organized formation of topologically correct
 feature maps. Biol Cybern 43:59–69
33. Barthel KU, Hezel N, Jung K, Schall K (2023) Improved evaluation
and generation of grid layouts using distance preservation qualityand linear assignment sorting. In: Computer graphics forum
34. Ma Y et al (2022) X-clip: end-to-end multi-grained contrastive
learning for video-text retrieval, pp 638-647. https://doi.org/10.
1145/3503161.3547910
35. Bain M, Nagrani A, Varol G, Zisserman A (2022) A cliphitchhiker’s
 guide to long video retrieval. arXiv:2205.08508
36. Ali A, Schwartz I, Hazan T, Wolf L (2022) Video and text matching
with conditioned embeddings, pp 1565–1574
37. Vaswani A et al (2017) Attention is all you need. In: Guyon I et al
(eds.) Advances in neural information processing systems, vol 30.
123
International Journal of Multimedia Information Retrieval (2024) 13 :15 Page 13 of 13 15
Curran Associates, Inc. https://proceedings.neurips.cc/paper_files/
paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf
38. Rossetto L, Gasser R, Sauter L, Bernstein A, Schuldt H, Lokoc
J et al (2021) A system for interactive multimedia retrievalevaluations. In: Lokoc J et al (eds.) International conference on mul-timedia modeling. Springer. https://doi.org/10.1007/978-3-03067835-7_33

39. Rossetto L, Schuldt H, Awad G, Butt AA, Kompatsiaris I et al
(2019) V3C—a research video collection. Kompatsiaris I, et al(eds.) International conference on multimedia modeling. Springer,pp 349–360. https://doi.org/10.1007/978-3-030-05710-7_2940. Lokoˇ c J et al (2019) Interactive search or sequential browsing?
A detailed analysis of the video browser showdown 2018. In:ACM transactions on multimedia computing, communications, andapplications, vol 15. https://doi.org/10.1145/3295663
41. Bird S, Klein E, Loper E (2009) Natural language processing with
Python: analyzing text with the natural language toolkit. O’ReillyMedia, Inc., Sebastopol
Publisher’s Note Springer Nature remains neutral with regard to jurisdictional
 claims in published maps and institutional affiliations.
"""

outputs = re.findall(r'\n[0-9]{1,2}\.\s.*?(?=\n[0-9]{1,2}\.\s|\Z)', references, re.DOTALL)
for output in outputs:
    print(output)

# i want each element in output to be a reference

# output = re.findall(r'\[\d+\].*?(?=\[\d+\]|\Z)', references, re.DOTALL)