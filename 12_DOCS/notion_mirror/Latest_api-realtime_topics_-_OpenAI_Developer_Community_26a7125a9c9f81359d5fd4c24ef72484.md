# Latest api-realtime topics - OpenAI Developer Community

> Notion URL: https://app.notion.com/p/Latest-api-realtime-topics-OpenAI-Developer-Community-26a7125a9c9f81359d5fd4c24ef72484
> Created: 2025-09-10T21:59:00.000Z
> Last edited: 2025-09-18T19:39:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
Welcome to the OpenAI Developer Community, a forum for developers to meet and chat with other developers while building with OpenAI’s APIs and developer platform.
This is not a place for ChatGPT discussion (with the exception of ChatGPT developer tools, like Codex). ChatGPT discussion takes place in the OpenAI Discord community.
What to know:
1. This forum is community-run and maintained. Not all posts are monitored. To get in touch with OpenAI, reach out at https://help.openai.com/en/?q=contact.
1. Discussions related to the ChatGPT app and plans will be hidden, and your account may be suspended. (We must keep conversations focused on technical topics related to building with OpenAI, for the sake of the larger community here.)
1. Before posting a new topic, please search the forum for similar topics. This prevents duplicate discussions.
1. Your use of this forum means you agree to the community guidelines, which include being nice, productive, and constructive. Read the full community guidelines: FAQ - OpenAI Developer Community
I’m encountering an issue with GPT-4o-Transcribe where, in some cases, the system returns a final output that is exactly the same as the input prompt provided in the configuration. I’m unsure why this happens, and I’d like to understand if this is a bug in the API.
I’ve noticed this behavior occurs more frequently with Spanish text. Is there a known limitation or condition that causes the model to return the unmodified prompt as the transcription result?
Here’s a summary of what I’m seeing:
- The final output is identical to the prompt.
- This happens intermittently.
- It severely affects the real-time transcription experience and makes it unsuitable for production use.
- For this test, I used a HyperX QuadCast microphone.
Below I’m including some API event logs that show this behavior, along with my session configuration for reference.
Let me know if there’s a workaround or if this is something the team is already aware of. I’d really appreciate any guidance on how to mitigate or avoid this issue.
Logs:
```plain text
Received message: {'type': 'input_audio_buffer.speech_started', 'event_id': 'event_BK4ZqecytxeVEAGTNsVMa', 'audio_start_ms': 3796, 'item_id': 'item_BK4Zqm01V3DvAZsu6hCt1'}
Received message: {'type': 'input_audio_buffer.speech_stopped', 'event_id': 'event_BK4ZrpiBrdUp2x8NQL0DX', 'audio_end_ms': 4960, 'item_id': 'item_BK4Zqm01V3DvAZsu6hCt1'}
Received message: {'type': 'input_audio_buffer.committed', 'event_id': 'event_BK4ZrAfYTpbGAOYL0G2L3', 'previous_item_id': 'item_BK4ZnE1K1NP0YgOYLMJ35', 'item_id': 'item_BK4Zqm01V3DvAZsu6hCt1'}
Received message: {'type': 'conversation.item.created', 'event_id': 'event_BK4ZrzhIZZBgxsefJPeJR', 'previous_item_id': 'item_BK4ZnE1K1NP0YgOYLMJ35', 'item': {'id': 'item_BK4Zqm01V3DvAZsu6hCt1', 'object': 'realtime.item', 'type': 'message', 'status': 'completed', 'role': 'user', 'content': [{'type': 'input_audio', 'transcript': None}]}}
Received message: {'type': 'conversation.item.input_audio_transcription.delta', 'event_id': 'event_BK4Zs1QyLEGUIY8HlWvak', 'item_id': 'item_BK4Zqm01V3DvAZsu6hCt1', 'content_index': 0, 'delta': 'Esta'}
Received message: {'type': 'conversation.item.input_audio_transcription.delta', 'event_id': 'event_BK4ZsuVpHgvR60LP5Isvn', 'item_id': 'item_BK4Zqm01V3DvAZsu6hCt1', 'content_index': 0, 'delta': ' es'}
Received message: {'type': 'conversation.item.input_audio_transcription.delta', 'event_id': 'event_BK4ZsDNjA8jfxZlzTCG0C', 'item_id': 'item_BK4Zqm01V3DvAZsu6hCt1', 'content_index': 0, 'delta': ' una'}
Received message: {'type': 'conversation.item.input_audio_transcription.delta', 'event_id': 'event_BK4Zswq1EW5fwM1DsIqw1', 'item_id': 'item_BK4Zqm01V3DvAZsu6hCt1', 'content_index': 0, 'delta': ' prueba'}
Received message: {'type': 'conversation.item.input_audio_transcription.delta', 'event_id': 'event_BK4ZsCTmm8YMZa3Oz27eb', 'item_id': 'item_BK4Zqm01V3DvAZsu6hCt1', 'content_index': 0, 'delta': ' para'}
Received message: {'type': 'conversation.item.input_audio_transcription.delta', 'event_id': 'event_BK4ZsSHnHgYY1M2Gw8cRX', 'item_id': 'item_BK4Zqm01V3DvAZsu6hCt1', 'content_index': 0, 'delta': ' mostrar'}
Received message: {'type': 'conversation.item.input_audio_transcription.delta', 'event_id': 'event_BK4ZsRiXuPJnE9V7NFA2p', 'item_id': 'item_BK4Zqm01V3DvAZsu6hCt1', 'content_index': 0, 'delta': ' el'}
Received message: {'type': 'conversation.item.input_audio_transcription.delta', 'event_id': 'event_BK4ZsUd2inA5KSKjNOJuW', 'item_id': 'item_BK4Zqm01V3DvAZsu6hCt1', 'content_index': 0, 'delta': ' bug'}
Received message: {'type': 'conversation.item.input_audio_transcription.delta', 'event_id': 'event_BK4ZsEEV9g764nTk5FJYr', 'item_id': 'item_BK4Zqm01V3DvAZsu6hCt1', 'content_index': 0, 'delta': ' de'}
Received message: {'type': 'conversation.item.input_audio_transcription.delta', 'event_id': 'event_BK4Zsmk7Pz4n1r3ju19rq', 'item_id': 'item_BK4Zqm01V3DvAZsu6hCt1', 'content_index': 0, 'delta': ' la'}
Received message: {'type': 'conversation.item.input_audio_transcription.delta', 'event_id': 'event_BK4ZsPugz89oEIS1amWCz', 'item_id': 'item_BK4Zqm01V3DvAZsu6hCt1', 'content_index': 0, 'delta': ' trans'}
Received message: {'type': 'conversation.item.input_audio_transcription.delta', 'event_id': 'event_BK4Zs9TbogfkvvqYQd2WL', 'item_id': 'item_BK4Zqm01V3DvAZsu6hCt1', 'content_index': 0, 'delta': 'cripción'}
Received message: {'type': 'conversation.item.input_audio_transcription.delta', 'event_id': 'event_BK4Zs0RNnmfrbRq27nfG4', 'item_id': 'item_BK4Zqm01V3DvAZsu6hCt1', 'content_index': 0, 'delta': '.'}
Received message: {'type': 'conversation.item.input_audio_transcription.completed', 'event_id': 'event_BK4Zs3IjOSOmW2CiDFGOq', 'item_id': 'item_BK4Zqm01V3DvAZsu6hCt1', 'content_index': 0, 'transcript': 'Esta es una prueba para mostrar el bug de la transcripción.'}

```
Config session:
```plain text
    session_config = {
        "type": "transcription_session.update",
        "session": {
            "input_audio_format": "pcm16",
            "input_audio_transcription": {
                "model": "gpt-4o-transcribe",
                "language": "es",
                "prompt": "Esta es una prueba para mostrar el bug de la transcripción.",
            },
            "turn_detection": {
                "type": "server_vad",
                "threshold": 0.5,
                "prefix_padding_ms": 300,
                "silence_duration_ms": 300,
            },
            "input_audio_noise_reduction": {"type": "near_field"},
        },
    }

```
I’ve similar issue with transcribing Japanese language
I am using audio book from Kokoro-Speech-Dataset
I use book chapter text as the prompt
I run the audio file with VAD (which will cut it into smaller segments)
the audio opening part contain some statement or information that is not in the prompt. and this is where the gpt-4o-transcribe is outputting all the prompt content
Experiencing the same issue. Seems to occur mostly when the audio has no speech, even if it has other noise. Not sure how we can easily filter this out before transcribing.
OpenAI Support - what can we do in the API call to work around this behaviour?
Same issue here. GPT-4o-Transcribe is sending transcription events rewriting the prompt exactly. With some prompts it happens every time, with others only occasionally. Maybe this is happening with non-English languages? I’m using Italian.
I didn’t find a workout other than removing the context prompt entirely, which is a shame.
Yes, I am getting this when the audio has no speech. I’m trying to mitigate it with using client side VAD and skip the open AI API call when there is no speech. But the VAD I’m using is not perfect, so I still get it sometimes.
