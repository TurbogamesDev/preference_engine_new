import helpers.entry_fetcher as EntryFetcher
import helpers.tag_scores_calculator as TagScoresCalculator
import helpers.normalised_score_assigner as NormalisedScoreAssigner
import helpers.output_handler as OutputHandler

parsed_entries_response = EntryFetcher.fetch_parsed_entries_response("turbogames")

if parsed_entries_response:
    print("Successfully retrieved entries from AniList!")

started_entries = parsed_entries_response.started_entries
not_started_medias = parsed_entries_response.not_started_media
media_to_watch_status = parsed_entries_response.media_to_watch_status

tag_scores = TagScoresCalculator.calculate_tag_scores(started_entries)

print("Calculated raw tag_scores.")

media_to_normalised_score = NormalisedScoreAssigner.calculate_media_to_normalised_score_dict(started_entries, not_started_medias, tag_scores)

print("Calculated normalised scored for anime.")

OutputHandler.generate_output_svg(media_to_normalised_score, not_started_medias)

print("Successfully generated output SVG!")

OutputHandler.append_log_file(media_to_normalised_score, parsed_entries_response)
OutputHandler.append_tag_score_log_file(tag_scores)

print("Successfully appended log files!")
