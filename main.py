import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# التوكن يتم قراءته من إعدادات Railway (Variables)
TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً دراكون، أنا جاهز للتصميم! أرسل لي فيديو.")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("جاري المعالجة...")
    
    file = await update.message.video.get_file()
    input_path = "input.mp4"
    output_path = "output.mp4"
    await file.download_to_drive(input_path)

    try:
        clip = VideoFileClip(input_path)
        # إضافة نص
        txt_clip = TextClip("Drakon Design", fontsize=50, color='white', font='Arial-Bold')
        txt_clip = txt_clip.set_pos('bottom').set_duration(clip.duration)
        
        video = CompositeVideoClip([clip, txt_clip])
        video.write_videofile(output_path, codec="libx264", audio_codec="aac")

        await update.message.reply_video(video=open(output_path, 'rb'))
    except Exception as e:
        await update.message.reply_text(f"خطأ: {str(e)}")
    finally:
        if os.path.exists(input_path): os.remove(input_path)
        if os.path.exists(output_path): os.remove(output_path)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    application.run_polling()
