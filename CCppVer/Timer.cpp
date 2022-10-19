#include <iostream>
#include <fstream>
#include <cstdint>
#include <string>
#include <algorithm>


class Timer
{
public:
    Timer(std::string sourcePath, std::string shiftedPath)
        : m_source(sourcePath), m_shiftedSubtitles(shiftedPath) 
    { }
    ~Timer()
    {
        m_source.close();
        m_shiftedSubtitles.close();
    }

    void shiftSubtitles(int32_t shiftBy)
    {
        shiftBy *= 1000;

        uint32_t textNumber = 1;

        std::string line, hour;
        std::string timeSplit;
        
        while(std::getline(m_source, line))
        {
            if(!(!line.empty() && std::all_of(line.begin(), line.end(), ::isdigit)) && textNumber != 1) 
            {
                m_shiftedSubtitles << line << std::endl;
                continue;
            }
            std::getline(m_source, hour);
            
            timeSplit = hour.substr(0, hour.find(" --> "));
            Timer::TimeParser parsed1stPart = parsTime(timeSplit);
            Timer::TimeParser shiftedParsed1stPart = shiftTime(parsed1stPart, shiftBy);

            timeSplit = hour.substr(hour.find(" --> ") + 5,
                                    hour.length() - hour.find(" --> ") - 5);
            Timer::TimeParser parsed2ndPart = parsTime(timeSplit);
            Timer::TimeParser shiftedParsed2ndPart = shiftTime(parsed2ndPart, shiftBy);

            m_shiftedSubtitles << textNumber << std::endl;
            
            m_shiftedSubtitles << shiftedParsed1stPart.printTime()
                                << " --> "
                                << shiftedParsed2ndPart.printTime()
                                << std::endl;

            textNumber += 1;
        }
    }

private:
    class TimeParser
    {
    public:
        TimeParser(int32_t hours, int32_t minutes, int32_t seconds, int32_t milliseconds)
            : m_hours(hours)
            , m_minutes(minutes)
            , m_seconds(seconds)
            , m_milliseconds(milliseconds)
        {}

        uint32_t getCollapsedTime()
        {
            return m_hours * 3600000
                 + m_minutes * 60000
                 + m_seconds * 1000
                 + m_milliseconds;
        }

        std::string printTime()
        {
            char formatedTime[m_timeFormat.length()+1];
            std::snprintf(formatedTime, m_timeFormat.length(), m_timeFormat.c_str(),
                m_hours, m_minutes, m_seconds, m_milliseconds);
            
            return formatedTime;
        }
    private:
        const std::string m_timeFormat = "%02d:%02d:%02d,%03d";
        int32_t m_hours, m_minutes, m_seconds, m_milliseconds;
    };

    std::ifstream m_source;
    std::ofstream m_shiftedSubtitles;

private:
    Timer::TimeParser parsTime(std::string& oldTime)
    {
        size_t firstColonAppearance = oldTime.find(':');
        int32_t hours = std::atoi(oldTime.substr(0, firstColonAppearance).c_str());
        int32_t minutes = std::atoi(oldTime.substr(firstColonAppearance + 1, 2).c_str());
        int32_t seconds = std::atoi(oldTime.substr(firstColonAppearance + 4, 2).c_str());
        int32_t millisecond = std::atoi(oldTime.substr(firstColonAppearance + 7, 3).c_str());
        return Timer::TimeParser(hours, minutes, seconds, millisecond);
    }

    Timer::TimeParser shiftTime(Timer::TimeParser time, int32_t shiftBy)
    {
        int32_t shiftedTime = time.getCollapsedTime() - shiftBy;
        if (shiftedTime < 0)
            return Timer::TimeParser(0, 0, 0, 0);
        return Timer::TimeParser(
            shiftedTime / 3600000 % 10000,
            shiftedTime % 3600000 / 60000,
            shiftedTime % 60000 / 1000,
            shiftedTime % 1000
        );
    }
};


int main()
{
    // char choice;
    // std::string file, newFile;
    // int32_t shiftBy;
    
    // std::cout << "Type of the file: " << std::endl;
    // std::cout << "With text line number - 1" << std::endl;
    // std::cout << "Without               - 2" << std::endl;

    // std::cout << "Choice: ";
    // std::cin >> choice;

    // std::cout << "File name: ";
    // std::cin >> file;

    // std::cout << "To what file write the output: ";
    // std::cin >> newFile;

    // std::cout << "Shift by what amount: ";
    // std::cin >> shiftBy;

    Timer test("ST1.srt", "ST1S.srt");

    test.shiftSubtitles(12);

    return 0;
}