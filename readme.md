 # The task is to recognize automatically the definition phrase in scientific articles, in French.
And in the context of generalisation of probabilistic methods, the best performance of this task is made with a rule method, developped by Thierry Hamon.

The rule method consists of two basic elements:
1, the markers;
2, the morphosyntaxique features.

And we begin with these assumptions of the morphosyntaxique features:
1, a phrase of definition contains a marker of definition for example: c'est-à-dire, défini comme;
2, scientific terms are mostly noun, like ADN, Context free grammar, and the definition of a scientific term tends to contain a 
noun chunk, too.

To sum up, this is how we do:

1, segmentation of text into phrases -- 2, find phrases containing markers -- 3, apply the chunker (treetagger) -- 4, find NOUN 
to the left and to the right of the marker -- 5, YES, this is a phrase of definition.

Quite brutal method right ? That's why we have a quite disappoiting performance, about 17% for precision, 30% for recall.

But simple, just two conditions: 1, marker in the phrase ? 2, NOUN in the left and right side of marker ?

Besides, we have additional tips, like:
1, a defining phrase is tend to be a long phrase, at lease more than 130 letters;
2, a defining phrase is mostly in the main part, rearly in the introduction nor conclusion;
3, generally, around the marker, the NOUN is quite nearby == the distance between the marker and the NOUN chunk, this is a third 
condition, ajustable for the outcome.


