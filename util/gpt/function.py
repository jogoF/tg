import asyncio
import openai


async def request(key, data, style):
    head = data[0]
    body = data[1]
    prompt1 = f"Заголовок для нативного поста {str(style).lower()} на русском языке для '{head}'"
    if {str(style).lower()}=="от первого лица":
        prompt2 = f"Нативный пост от лица девушки маркетолога длинной не более 120 символов(это важно!) в разговорной форме про положительные свойства товара описанного в этом тексте: {body}"
    else:
        prompt2 = f"Генерируйте рекламный продающий текст в стиле {str(style).lower()} на русском языке длиной не более 50 слов(это важно!) на основе текста чтобы пост легко читался и был кратким и локоничным: {body}"
    openai.api_key = key
    response1 = await openai.ChatCompletion.acreate(model="gpt-3.5-turbo", messages=[{"role": "assistant", "content": prompt1}])
    response2 = await openai.ChatCompletion.acreate(model="gpt-3.5-turbo", messages=[{"role": "assistant", "content": prompt2}])
    return [str(response1.choices[0].message.content).replace('"', ''), str(response2.choices[0].message.content).replace('"', '')]



a = [1,2,3]

