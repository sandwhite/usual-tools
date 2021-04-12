#include"file_delete.h"

using namespace std;

namespace DJ
{
	file_delete::file_delete()
	{
	}

	file_delete::~file_delete()
	{
	}

	SYSTEMTIME file_delete::GetFolderCreateTime(CString sFolder)
	{
		SYSTEMTIME screatetime;
		HANDLE hDir;
		hDir = CreateFile(sFolder, GENERIC_READ, FILE_SHARE_READ | FILE_SHARE_DELETE, NULL,
			OPEN_EXISTING, FILE_FLAG_BACKUP_SEMANTICS, NULL);//���ִ�Ŀ¼ ֻ����ʽ�򿪼���

		FILETIME lpCreateTime, lpAccessTime, lpWriteTime;//����ʱ�䣬����ʱ�䣬�޸�ʱ��
		if (GetFileTime(hDir, &lpCreateTime, &lpAccessTime, &lpWriteTime))
		{
			FILETIME fcreatetime;
			FileTimeToLocalFileTime(&lpCreateTime, &fcreatetime);//ת��Ϊ����ʱ��
			FileTimeToSystemTime(&fcreatetime, &screatetime);//ת��Ϊϵͳʱ��
		}

		CloseHandle(hDir);//�ر��ļ����

		return screatetime;
	}

	//��ȡ�ļ�����޸�����
	bool file_delete::GetFileModifyDate(CString filePathName, SYSTEMTIME &modDate)
	{
		HANDLE   hFile;
		WIN32_FIND_DATA   wfd;
		SYSTEMTIME   systime;
		FILETIME   localtime;

		memset(&wfd, 0, sizeof(wfd));
		if ((hFile = FindFirstFile(filePathName, &wfd)) == INVALID_HANDLE_VALUE)
			return false;
		//ת��ʱ��  
		FileTimeToLocalFileTime(&wfd.ftLastWriteTime, &localtime);
		FileTimeToSystemTime(&localtime, &systime);

		modDate = systime;
		return true;
	}

	//ת��ʱ������
	time_t file_delete::TimeConvertToSec(int year, int month, int day)
	{
		tm info = { 0 };
		info.tm_year = year - 1900;
		info.tm_mon = month - 1;
		info.tm_mday = day;
		return mktime(&info);
	}

	//�������������������
	int file_delete::DaysOffset(int fYear, int fMonth, int fDay, int tYear, int tMonth, int tDay)
	{
		int fromSecond = (int)TimeConvertToSec(fYear, fMonth, fDay);
		int toSecond = (int)TimeConvertToSec(tYear, tMonth, tDay);
		return (toSecond - fromSecond) / 24 / 3600;
	}

	//ɾ��Ŀ¼�µ��ļ����ļ���
	bool file_delete::DeleteDirectory(CString directory_path)
	{
		CFileFind finder;
		CString path;
		path.Format(_T("%s\\*.*"), directory_path);
		BOOL bWorking = finder.FindFile(path);
		while (bWorking)
		{
			bWorking = finder.FindNextFile();
			if (finder.IsDirectory() && !finder.IsDots())//�����ļ���
			{
				//�ݹ�ɾ���ļ���
				DeleteDirectory(finder.GetFilePath());
				RemoveDirectory(finder.GetFilePath());

			}
			else//ɾ���ļ�
			{
				DeleteFile(finder.GetFilePath());
			}
		}
		RemoveDirectory(directory_path);

		return true;
	}

	//ɾ��ָ���ļ���Ŀ¼��ȫ����ʱ�ļ� 

	void file_delete::DeleteAllFile(CString strDir, int days)
	{

		if (days < 0)
			days = 30;
		SYSTEMTIME curDate;
		GetLocalTime(&curDate); //��ȡ��ǰʱ��
		CFileFind   finder;
		BOOL   bFound = finder.FindFile(strDir + L"\\*", 0);
		while (bFound)
		{
			bFound = finder.FindNextFile();
			if (finder.GetFileName() == "." || finder.GetFileName() == "..")
				continue;
			//   ȥ���ļ�(��)ֻ��������
			SetFileAttributes(finder.GetFilePath(), FILE_ATTRIBUTE_NORMAL);
			if (finder.IsDirectory())
			{
				SYSTEMTIME fDate = GetFolderCreateTime(finder.GetFilePath());  //��ȡ�ļ�����޸�ʱ��
				int dayOffset = DaysOffset(fDate.wYear, fDate.wMonth, fDate.wDay,
					curDate.wYear, curDate.wMonth, curDate.wDay);
				if (dayOffset > days)
				{
					DeleteDirectory(finder.GetFilePath());
				}
			}
			else
			{
				SYSTEMTIME fDate;
				if (GetFileModifyDate(finder.GetFilePath(), fDate))  //��ȡ�ļ�����޸�ʱ��
				{
					int dayOffset = DaysOffset(fDate.wYear, fDate.wMonth, fDate.wDay,
						curDate.wYear, curDate.wMonth, curDate.wDay);
					if (dayOffset > days)
						DeleteFile(finder.GetFilePath());
				}
			}
		}
		finder.Close();
		//  Ȼ��ɾ�����ļ���
	   // RemoveDirectory(strDir);
	}
}

//int main()
//
//{
//	
//	CString file_path = "C:/Users/Administrator/Desktop/pic";
//	int beforedays = 0;
//
//	//ɾ������Ŀ¼��5��ǰ�����ļ�������Ŀ¼��
//	DeleteAllFile(file_path, beforedays);
//	
//	return 0;
//}



