import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# التوكن الخاص بك
TOKEN = "8854820353:AAHAvD18ooi032u58LvPnwT2bQLPy4o5VU4"

# إعداد السجلات لمتابعة عمل البوت
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك، أنا دراكون، بوت تصميم الفيديوهات الخاص بك. أرسل لي أي فيديو وسأقوم بتعديله!")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("جاري استلام ومعالجة الفيديو، يرجى الانتظار يا دراكون...")

    # تحميل الفيديو من تلجرام
    video_file = await update.message.video.get_file()
    input_path = "input_video.mp4"
    output_path = "output_video.mp4"
    await video_file.download_to_drive(input_path)

    try:
        # معالجة الفيديو: إضافة نص
        clip = VideoFileClip(input_path)
        
        # إضافة نص "Drakon Design"
        txt_clip = TextClip("Drakon Design", fontsize=50, color='white', font='Arial-Bold')
        txt_clip = txt_clip.set_pos('bottom').set_duration(clip.duration)
        
        video = CompositeVideoClip([clip, txt_clip])
        video.write_videofile(output_path, codec="libx264", audio_codec="aac")

        # إرسال النتيجة
        await update.message.reply_video(video=open(output_path, 'rb'))
        
        # تنظيف الملفات المؤقتة
        clip.close()
        os.remove(input_path)
        os.remove(output_path)
        
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ أثناء التصميم: {str(e)}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    
    print("بوت دراكون يعمل الآن...")
    application.run_polling()
