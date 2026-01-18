---
title: "The Relational Self: Where Do I End and We Begin?"
date: 2025-01-18
description: "Exploring whether identity lives inside us or between us—through philosophy and research."
---

There's a question I keep returning to: **Is the self something I have, or something that happens between people?**

Western culture tells me I'm an individual first. My identity is inside me—my traits, my values, my essence. Relationships are things I *have*, not things I *am*.

But other traditions disagree. And so does a growing body of research.

## Three Philosophical Views

### The Western Individual

Descartes started with "I think, therefore I am"—the self as a thinking thing, separate from world and others. This view runs deep in Western culture: identity is internal, stable, discoverable through introspection.

From this perspective, I'm the same person whether I'm alone or with others. Context changes; I don't.

**The appeal**: It gives us ownership of ourselves. Agency. Responsibility.

**The problem**: It doesn't match how identity actually feels—shifting with context, shaped by relationships, never quite the same twice.

### The Relational View

Buddhist philosophy challenges the idea of a fixed self (*anatta*—"non-self"). What we call "self" is a process, not a thing. It arises in relationship and dissolves when conditions change.

Ubuntu philosophy from Southern Africa puts it directly: *"I am because we are."* The self is constituted through community. You don't exist as a person outside of relationships.

Confucian thought defines the self through roles—son, friend, citizen. To be a self is to be in right relationship with others.

**The appeal**: It matches the experience of being shaped by the people around us.

**The problem**: It can feel like losing yourself—if identity depends on others, who are you when alone?

### The Process View

Heraclitus said you can't step in the same river twice. The river is a pattern of flow, not a fixed thing.

Maybe the self is similar. Not a thing to find, but a pattern to notice. It emerges in context, changes across time, and never holds still long enough to pin down.

**The appeal**: It dissolves the either/or. Identity is neither purely internal nor purely external—it's a process that happens in the space between.

**What this means to me**: I find this view most honest. I'm not the same person with everyone. That's not inauthenticity—it's what selves actually do.

## What the Research Says

Philosophy gives us frameworks. Research gives us data.

### We See Ourselves Through Others' Eyes

Cooley (1902) called this the "looking-glass self": we form our self-concept by imagining how others see us.

Shrauger & Schoeneman (1979) tested this across 60 studies:

| Correlation | Strength |
|-------------|----------|
| Self-perception ↔ *perceived* other-perception | r = 0.40-0.60 |
| Self-perception ↔ *actual* other-perception | r = 0.20-0.40 |

**In plain terms**: We're more influenced by what we *imagine* others think than by what they actually think. Our self-image is built on imagination, not reality.

**What this means**: The self isn't discovered through introspection—it's constructed through social imagination. The mirror we look into is partly made of projections.

### Who We're With Shapes Who We Become

Eagle, Pentland, & Lazer (2009) tracked 94 people for 9 months using mobile phone data:

| Signal | Correlation with self-reported friendship |
|--------|------------------------------------------|
| Face-to-face time | r = 0.52 |
| Reciprocal calls | r = 0.58 |
| Location overlap | r = 0.35 |

Combined, proximity signals predicted friendship with 95% accuracy.

**In plain terms**: Relationships aren't just feelings—they're patterns. Who you spend time with, and who reciprocates, predicts who you'd call a friend.

**What this means**: Relationships are structural, not just emotional. And structure shapes identity. We become like the people we're around.

### Network Position Predicts Outcomes

Burt (1992, 2004) studied how social network position affects life outcomes:

| Position | Effect |
|----------|--------|
| Bridging disconnected groups | Promoted 1.4 years earlier |
| High-constraint (dense network) | 45% had ideas rated "good" |
| Low-constraint (bridging) | 72% had ideas rated "good" |

**In plain terms**: Where you sit in the social network—not just who you know, but how those people connect to each other—predicts success and creativity.

**What this means**: Identity isn't just about who you are, but where you are in the web of relationships. Position shapes possibility.

### Social Networks Seek Balance

Heider (1958) proposed that relationships tend toward equilibrium. Leskovec et al. (2010) tested this on 100,000+ users:

| Triad type | Expected | Observed |
|------------|----------|----------|
| All friends (+++) | 12.5% | 35.2% |
| Two friends, one enemy (++-) | 37.5% | 38.1% |
| One friend, two enemies (+--) | 37.5% | 21.8% |
| All enemies (---) | 12.5% | 4.9% |

73% of triads were balanced (vs. 50% expected by chance).

**In plain terms**: "The friend of my friend is my friend" isn't just folk wisdom—it's statistically measurable. Social networks evolve toward stable configurations.

**What this means**: There's pressure toward coherence in our relationships. Navigating between disconnected worlds creates structural tension, not just emotional tension.

### Your Relational Style Is Stable

Saramäki et al. (2014) tracked how people maintain relationships over 18 months:

| Property | Stability |
|----------|-----------|
| Network size | r = 0.95 |
| Tie strength distribution | r = 0.87 |
| Top 5 contacts persistence | 72% |

**In plain terms**: The *shape* of how you distribute attention across relationships stays remarkably stable, even as specific relationships change.

**What this means**: We each have a relational signature—a pattern of how we connect. Understanding this pattern might be as revealing as understanding personality traits.

Dunbar (1992) identified consistent layers:

| Circle | Typical size | Contact frequency |
|--------|--------------|-------------------|
| Support clique | 5 | Weekly |
| Sympathy group | 15 | Monthly |
| Active network | 150 | Yearly |

These layers appear across cultures. We seem to have cognitive limits on how many relationships we can maintain at different depths.

## The Privacy Problem

This research has a shadow side.

Jernigan & Mistree (2009) showed that social network patterns can reveal things people haven't disclosed:
- Sexual orientation predictable from friend networks (AUC = 0.78)
- No explicit disclosure required

**What this means**: Relationship data is sensitive data. Patterns speak even when people don't. The power to observe relationships is the power to expose what people might want to keep private.

This shapes how I think about taocore-human. Detecting relational patterns isn't neutral. It carries responsibility.

## So Are My Relationships Part of Me?

After sitting with this question:

**My relationships are part of me the way language is.** I didn't choose Mandarin or English—they were given to me by context. But they shape how I think, what I can express, who I can connect with. They're not external to me; they're woven into how I experience the world.

**The different versions of me are all real.** I'm not the same person in every context. That's not performance or inauthenticity—it's what selves do. The philosopher William James said we have as many social selves as there are people who recognize us. I think he was right.

**The tension is also me.** If you move between different worlds—cultures, communities, generations—you feel the pull of multiple belongings. That tension isn't a failure of identity. It's what identity feels like when it's relational.

## What This Means for taocore-human

For the system I'm building:

**Extract** (with uncertainty):
- Co-occurrence patterns
- Network centrality
- Proximity signals
- Synchrony indicators

**Report** (honestly):
- Numbers with confidence intervals
- Pattern descriptions, not relationship labels
- What cannot be determined

**Refuse**:
- Relationship type classifications
- Quality judgments
- Predictions about individuals
- Anything that could expose what people haven't chosen to reveal

## A Closing Thought

The question "who am I?" might be less useful than "who am I with whom?"

Identity isn't a thing to find. It's a pattern that emerges in relationship—with others, with context, with time. Observable behavior traces this pattern imperfectly. What we see is real, but it's not the whole.

The reflection on the water is not the water.

---

## References

Burt, R. S. (1992). *Structural Holes*. Harvard University Press.

Burt, R. S. (2004). Structural holes and good ideas. *American Journal of Sociology*, 110(2), 349-399.

Cooley, C. H. (1902). *Human Nature and the Social Order*. Scribner's.

Dunbar, R. I. M. (1992). Neocortex size as a constraint on group size. *Journal of Human Evolution*, 22(6), 469-493.

Eagle, N., Pentland, A., & Lazer, D. (2009). Inferring friendship network structure. *PNAS*, 106(36), 15274-15278.

Heider, F. (1958). *The Psychology of Interpersonal Relations*. Wiley.

Jernigan, C., & Mistree, B. F. (2009). Gaydar: Facebook friendships expose sexual orientation. *First Monday*, 14(10).

Leskovec, J., et al. (2010). Predicting positive and negative links in online social networks. *WWW*, 641-650.

Saramäki, J., et al. (2014). Persistence of social signatures in human communication. *PNAS*, 111(3), 942-947.

Shrauger, J. S., & Schoeneman, T. J. (1979). Symbolic interactionist view of self-concept. *Psychological Bulletin*, 86(3), 549-573.
