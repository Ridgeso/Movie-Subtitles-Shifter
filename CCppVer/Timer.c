#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <ctype.h>

struct TimeParser_t
{
    int32_t hours, minutes, seconds, milliseconds;
};
typedef struct TimeParser_t TimeParser_t;

struct Timer_t
{
    char* source;
    char* shiftedSubtitles;
};
typedef struct Timer_t Timer_t;

uint32_t getCollapsedTime(TimeParser_t* parser)
{
    return parser->hours * 3600000
         + parser->minutes * 60000
         + parser->seconds * 1000
         + parser->milliseconds;
}

TimeParser_t parsTime(char* oldTime)
{
    int32_t hours = atoi(strtok(oldTime, ":,"));
    int32_t minutes = atoi(strtok(NULL, ":,"));
    int32_t seconds = atoi(strtok(NULL, ":,"));
    int32_t millisecond = atoi(strtok(NULL, ":,"));

    TimeParser_t parser = {hours, minutes, seconds, millisecond};
    return parser;
}

TimeParser_t shiftTime(TimeParser_t* time, int32_t shiftBy)
{
    int32_t shiftedTime = getCollapsedTime(time) - shiftBy;
    if (shiftedTime < 0)
        return (TimeParser_t){0, 0, 0, 0};
        
    return (TimeParser_t){
        shiftedTime / 3600000 % 10000,
        shiftedTime % 3600000 / 60000,
        shiftedTime % 60000 / 1000,
        shiftedTime % 1000
    };
}

int8_t isTextNumber(const char* text)
{
    if (!*text)
        return 0;

    char* c = (char*)text;
    while (*c)
    {
        if (!isdigit(*c))
            return 0;
        c++;
    }
    return 1;
}

void shiftSubtitles(Timer_t* timer, int32_t shiftBy)
{
    shiftBy *= 1000;
    FILE* source = fopen(timer->source, "r");
    FILE* shiftedSubtitles = fopen(timer->shiftedSubtitles, "w");

    if (source == NULL || shiftedSubtitles == NULL)
    {
        puts("Could not find source or could not create a new file.");
        return;
    }

    uint32_t textNumber = 1;

    ssize_t textLen;
    size_t lineLen = 0;
    char* line = NULL;
    size_t hourLen = 0;
    char* hour = NULL;
    char* timeSplit;
        
    while ((textLen = getline(&line, &lineLen, source)) != -1)
    {
        line[textLen - 1] = '\0';

        if(!(isTextNumber(line)) && textNumber != 1) 
        {
            fprintf(shiftedSubtitles, "%s\n", line);
            continue;
        }

        textLen = getline(&hour, &hourLen, source);
        hour[textLen - 1] = '\0';

        timeSplit = strstr(hour, " --> ");
        *timeSplit = '\0';
        timeSplit += 5;

        TimeParser_t parsed1stPart = parsTime(hour);
        TimeParser_t shifted1stHalf = shiftTime(&parsed1stPart, shiftBy);

        TimeParser_t parsed2ndPart = parsTime(timeSplit);
        TimeParser_t shifted2ndHalf = shiftTime(&parsed2ndPart, shiftBy);

        fprintf(shiftedSubtitles, "%d\n%02d:%02d:%02d,%03d --> %02d:%02d:%02d,%03d\n",
            textNumber,
            shifted1stHalf.hours, shifted1stHalf.minutes, shifted1stHalf.seconds, shifted1stHalf.milliseconds,
            shifted2ndHalf.hours, shifted2ndHalf.minutes, shifted2ndHalf.seconds, shifted2ndHalf.milliseconds);

        textNumber += 1;
    }

    free(line);
    free(hour);
    fclose(source);
    fclose(shiftedSubtitles);
}

int main()
{
    Timer_t test = {"ST1.srt", "ST1S.srt"};

    shiftSubtitles(&test, 12);

    return 0;
}