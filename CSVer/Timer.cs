using System;
using System.IO;

namespace Timer
{
    class Timer
    {
        private string m_sourcePath;
        private string m_shiftedSubtitlesPath;

        struct TimerParser
        {
            public int hours, minutes, seconds, milliseconds;
            public TimerParser(int h, int m, int s, int ms)
            {
                hours = h;
                minutes = m;
                seconds = s;
                milliseconds = ms;
            }

            public int CollapsedTime
            {
                get { return hours * 3600000 + minutes * 60000 + seconds * 1000 + milliseconds; }
                set
                {
                    hours = value / 3600000 % 10000;
                    minutes = value % 3600000 / 60000;
                    seconds = value % 60000 / 1000;
                    milliseconds = value % 1000;
                }
            }
            public string Time
            {
                get { return String.Format("{0:D2}:{1:D2}:{2:D2},{3:D3}",
                    hours, minutes, seconds, milliseconds); }
            }
        }

        public Timer(string sourcePath, string shiftedSubtitlesPath)
        {
            m_sourcePath = sourcePath;
            m_shiftedSubtitlesPath = shiftedSubtitlesPath;
        }

        public void ShiftSubtitles(int shiftBy)
        {
            shiftBy *= 1000;

            uint curentLine, textNumber = 1;

            using (StreamReader source = new StreamReader(m_sourcePath))
            { using (StreamWriter shiftedSubtitles = new StreamWriter(m_shiftedSubtitlesPath))
            {
                string line;
                while ((line = source.ReadLine()) != null)
                {
                    if (! (UInt32.TryParse(line, out curentLine) && curentLine == textNumber))
                    {
                        shiftedSubtitles.WriteLine(line);
                        continue;
                    }
                    
                    string hour = source.ReadLine();

                    string[] hourParts = hour.Split(' ');

                    TimerParser startTime = parseTime(hourParts[0]);
                    Console.Write(startTime.Time + " --> ");
                    TimerParser startTimeShifted = shiftTime(startTime, shiftBy);
                    Console.WriteLine(startTimeShifted.Time);

                    TimerParser endTime = parseTime(hourParts[2]);
                    TimerParser endTimeShifted = shiftTime(endTime, shiftBy);

                    shiftedSubtitles.WriteLine(String.Format("{0}\n{1} --> {2}",
                        textNumber, startTimeShifted.Time, endTimeShifted.Time));

                    textNumber++;
                }
            }
            }
        }

        private TimerParser parseTime(string time)
        {
            string[] tokens = time.Split(':', ',');
            foreach (string t in tokens)
            {
                Console.Write(t + ", ");
            }

            return new TimerParser(
                Int32.Parse(tokens[0]),
                Int32.Parse(tokens[1]),
                Int32.Parse(tokens[2]),
                Int32.Parse(tokens[3])
            );
        }

        private TimerParser shiftTime(TimerParser time, int shiftBy)
        {
            int shiftedTime = time.CollapsedTime - shiftBy;

            if (shiftedTime < 0)
                return new TimerParser(0, 0, 0, 0);

            time.CollapsedTime = shiftedTime;
            return time;
        }
    }

    class App
    {
        static void Main(string[] args)
        {
            Timer worker = new Timer(@"ST1.srt", @"ST1S.srt");

            worker.ShiftSubtitles(12);
        }
    }
}