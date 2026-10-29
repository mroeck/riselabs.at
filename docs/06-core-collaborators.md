# Core collaborators

How to invite someone to be listed on the site, what to collect, and what to
keep afterwards.

## The distinction this rests on

The site has two kinds of person, set by the `group` field in the file:

| `group` | Who | Shown as |
| --- | --- | --- |
| `rise` | People of the institute | "RISE" on their card |
| `collaborator` | People we work with closely who are **employed elsewhere** | "Core collaborator · <org>" on their card |

A collaborator must also carry an `org` line naming where they actually sit.

**One grid, not two.** Since October 2026 everyone appears in a single list on
the team page, ordered `rise` first and then `collaborator`, with **the
employer printed on every card**. Two separate sections made the
collaborators read as a lesser tier, which is not what the distinction is
for.

**Do not blur the two groups.** The distinction is what protects everyone: the
collaborator, whose employer has not endorsed RISE; RISE, because a site that
sells commissioned research should not imply a bench of people it cannot
deploy; and the reader, who can see what the institute actually is. The
employer line is what carries it now, and a sentence under the grid says so:
"Team members employed elsewhere are shown with their employer." Keep both.

## Before inviting anyone

Settle three things, once, and the rest is mechanical.

**1. The criterion.** Who qualifies, and therefore who does not. Collaborators
talk to each other, and an unexplained omission reads as a judgement. A
stateable rule - "a named role in a current or recent RISE project" - makes
absences impersonal. Write the rule down here when you have it.

**2. Their employer's position.** Anyone at a university, a ministry or a
consultancy may need to clear it, or may need wording that avoids implying
institutional endorsement. State the person's own role and organisation as
plain fact. Do not let page layout imply their institution is a RISE partner
unless it genuinely is.

**3. What happens when it ends.** Decide now whether a page comes down or gets
marked as past collaboration. Say which in the invitation.

## The invitation

Send one email that doubles as the consent record. Publishing someone's name,
photo, role and employer is processing personal data, and the lawful basis is
their consent. If the agreement sits in a reply to an email that plainly
states what will be published, where, and that they can withdraw at any time,
the record exists without anyone signing anything.

**Keep the replies.** That is the record.

The email must state:

- exactly what will appear - name, role, organisation, photo, short profile,
  links, and the automatic list of RISE projects and publications they are
  named on;
- that they are listed as employed elsewhere and not part of RISE;
- that nothing is published until they have approved the exact wording;
- that they can change or withdraw it at any time, without discussion;
- who to contact, and what happens if they move on.

Offer to draft the profile from their existing bio. This is the line that
converts: people agree in principle and then never write the three sentences.

## What to collect

| Field | Notes |
| --- | --- |
| `name` | As they want it written, including title if they use one |
| `role` | Their own role, at their own organisation |
| `org` | Required for collaborators |
| `portrait` | Square, at least 600 × 600 px. Save to `assets/img/people/`. Without one, the card shows their initials |
| `tagline` | One line in their own words; a note above 140 characters, a failure above 220 on why they do this work. Shown on the card and as the lede on their profile |
| `works_on` | Theme slugs from `_data/themes.yml`. A closed vocabulary; the checker rejects anything else |
| `also` | A second standing role that is not their day job - an IPCC author role, a report coordinating authorship. Optional |
| `summary` | One sentence, shown under their name |
| body text | Two or three sentences in their own voice |
| `links` | LinkedIn, Google Scholar, ORCID, personal site - whichever they want |
| `cite` | How their name appears in author lists, e.g. `Di Santo N` |

`cite` matters more than it looks: it is what underlines their name
automatically in the author list of every publication they are on.

## Publishing one

1. Copy `_people/example-colleague.md` to `_people/firstname-lastname.md`.
2. Fill it in. Set `group: collaborator` and add the `org` line.
3. Save the portrait to `assets/img/people/firstname-lastname.jpg`.
4. Delete the `published: false` line **only once there are no `[ADD]`
   placeholders left and the person has approved the text**.
5. Run `python3 docs-check.py`.

## Sequencing

The team page went live in October 2026 with Martin only. The rest appear as
each person approves their own text, which is the rule below and is not
negotiable for the sake of a fuller-looking page.

A person without a photograph gets their initials on a token-coloured square,
never a stock face.

## Review

Check the list about once a year: roles change, people move, links rot. A
profile that is wrong about where someone works is worse than no profile.
