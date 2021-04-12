#include "json_function.h"
#include<string>

#include"json/json.h"
#include<iostream>
#include<fstream>

namespace mine
{
	JsonFunction::JsonFunction() {}
	JsonFunction::~JsonFunction() {}
	
	std::string JsonFunction::WriteJson(Json::Value &root)
	{
		Json::StreamWriterBuilder writerBuilder;
		std::ostringstream os;
		std::unique_ptr<Json::StreamWriter> jsonWriter(writerBuilder.newStreamWriter());
		//1
		root["Cam_ID"] = Cam_ID;                                            //���ID
		root["Interface_Client_Address"] = Interface_Client_Address;         // ͼ����ͻ��˵�ַ
		root["Interface_Client_Port"] = Interface_Client_Port;               //ͼ����ͻ��˶˿�
		root["Control_Signal"] = Control_Signal;                            //�����źţ���ʼ����ͣ��ֹͣ����������
		root["ErrorCode"] = ErrorCode;                                      //�������
		root["LayerHeight"] = LayerHeight;                                  //��ǰ���
		root["CaptureFov"] = CaptureFov;                                    // ��ǰ�ӳ�
		root["CaptureDistance"] = CaptureDistance;                          //���ռ��
		root["CaptureFovRatio"] = CaptureFovRatio;                            // �����ӳ��ı���
		root["TruckLength"] = TruckLength;                                    // ����
		root["TruckBreadth"] = TruckBreadth;                                  //����
		root["CaptureDistanceMargin"] = CaptureDistanceMargin;                // ���ռ��������ֵ
		root["TruckCornerPoint1_x"] = var_float;                        // �����Ľǵ�1
		root["TruckCornerPoint1_y"] = var_float;                        // �����Ľǵ�1

		root["TruckCornerPoint2_x"] = var_float;                        // �����Ľǵ�2
		root["TruckCornerPoint2_y"] = var_float;                        // �����Ľǵ�2

		root["TruckCornerPoint3_x"] = var_float;                        // �����Ľǵ�3
		root["TruckCornerPoint3_y"] = var_float;                        // �����Ľǵ�3

		root["TruckCornerPoint4_x"] = var_float;                        // �����Ľǵ�4
		root["TruckCornerPoint4_y"] = var_float;                        // �����Ľǵ�4

		root["SafePos_x"] = var_float;                                            //��ȫ��,�̶�ֵ����Ϊ���ò���д��
		root["SafePos_y"] = var_float;                                            //��ȫ��,�̶�ֵ����Ϊ���ò���д��
		root["SafePos_z"] = var_float;                                            //��ȫ��,�̶�ֵ����Ϊ���ò���д��
		root["SafePos_c"] = var_float;                                            //��ȫ��,�̶�ֵ����Ϊ���ò���д��

		root["ReCheckPos_x"] = var_float;                                       //���ζ�λ�㣬�̶�ֵ����Ϊ���ò���д��
		root["ReCheckPos_y"] = var_float;                                       //���ζ�λ�㣬�̶�ֵ����Ϊ���ò���д��
		root["ReCheckPos_z"] = var_float;                                       //���ζ�λ�㣬�̶�ֵ����Ϊ���ò���д��
		root["ReCheckPos_c"] = var_float;                                       //���ζ�λ�㣬�̶�ֵ����Ϊ���ò���д��

		root["BoxRefPoint1_x"] = var_float;                                   // �Ͽ�1����ϵԭ��
		root["BoxRefPoint1_y"] = var_float;                                   // �Ͽ�1����ϵԭ��
		root["BoxRefPoint1_z"] = var_float;                                   // �Ͽ�1����ϵԭ��
		root["BoxRefPoint1_c"] = var_float;                                   // �Ͽ�1����ϵԭ��

		root["BoxRefPoint2_x"] = var_float;                                   // �Ͽ�2 ����ϵԭ��
		root["BoxRefPoint2_y"] = var_float;                                   // �Ͽ�2 ����ϵԭ��
		root["BoxRefPoint2_z"] = var_float;                                   // �Ͽ�2 ����ϵԭ��
		root["BoxRefPoint2_c"] = var_float;                                   // �Ͽ�2 ����ϵԭ��


		//2 ʵʱ����
		root["CapturePointCurrent_x"] = var_float;     //��ǰ���յ�
		root["CapturePointCurrent_y"] = var_float;     //��ǰ���յ�

		root["PickPosCurrent_x"] = var_float;                                //��ǰץȡ��
		root["PickPosCurrent_y"] = var_float;                                //��ǰץȡ��
		root["PickPosCurrent_z"] = var_float;                                //��ǰץȡ��
		root["PickPosCurrent_c"] = var_float;                                //��ǰץȡ��

		root["BoxLength"] = var_float;                                           //������
		root["BoxBreadth"] = var_float;                                        //������
		root["Pos_queue_x"] = var_float;                                           //ץȡ��λ������
		root["Pos_queue_y"] = var_float;                                           //ץȡ��λ������
		root["Pos_queue_z"] = var_float;                                           //ץȡ��λ������
		root["Pos_queue_c"] = var_float;                                           //ץȡ��λ������
		root["CapturePoint_x"] = var_float;                                     //���յ�����
		root["CapturePoint_y"] = var_float;                                     //���յ�����



		//3 plc��ַ
														   //���ۻ�����ID
		root["AdrActPos_ByteDeviation"] = var_all;                                     //��ǰλ��
		root["AdrActPos_BitDeviation"] = var_all;

		root["AdrPickPos_ByteDeviation"] = var_all;                                     //ץȡλ��
		root["AdrPickPos_BitDeviation"] = var_all;

		root["AdrPlacePos_ByteDeviation"] = var_all;                                     //����λ��
		root["AdrPlacePos_BitDeviation"] = var_all;

		root["AdrState_ByteDeviation"] = var_all;                                     //״̬
		root["AdrState_BitDeviation"] = var_all;

		root["TransitionPoint1_ByteDeviation"] = var_all;                                     //���ɵ�1
		root["TransitionPoint1_BitDeviation"] = var_all;

		root["TransitionPoint2_ByteDeviation"] = var_all;                                     //���ɵ�2
		root["TransitionPoint2_BitDeviation"] = var_all;


		//4 plcdata address		

		root["AdrCapPos_ByteDeviation"] = var_all;                                         //��ǰλ��	
		root["AdrCapPos_BitDeviation"] = var_all;


		root["AdrReCheckPos_ByteDeviation"] = var_all;                                     //����λ��
		root["AdrReCheckPos_BitDeviation"] = var_all;


		root["CylinderPos1_ByteDeviation"] = var_all;                                     //����1λ��
		root["CylinderPos1_BitDeviation"] = var_all;


		root["CylinderPos2_ByteDeviation"] = var_all;                                     //����2λ��
		root["CylinderPos2_BitDeviation"] = var_all;
		// DI


		root["AdrCarInPosition_ByteDeviation"] = var_all;                                     //ͣ����λ�ź�
		root["AdrCarInPosition_BitDeviation"] = var_all;


		root["bVacuum_ByteDeviation"] = var_all;                                     //��տ����ź�
		root["bVacuum_BitDeviation"] = var_all;


		root["AdrEmptyBox1_ByteDeviation"] = var_all;                                     //����1���
		root["AdrEmptyBox1_BitDeviation"] = var_all;


		root["AdrEmptyBox2_ByteDeviation"] = var_all;                                     //����2���
		root["AdrEmptyBox2_BitDeviation"] = var_all;


		root["AdrEmptyBox3_ByteDeviation"] = var_all;                                     //����3���
		root["AdrEmptyBox3_BitDeviation"] = var_all;


		root["AdrEmptyBox4_ByteDeviation"] = var_all;                                     //����4���
		root["AdrEmptyBox4_BitDeviation"] = var_all;


		//DO
		root["AdrSuckerStart_ByteDeviation"] = var_all;                                 //���̿���
		root["AdrSuckerStart_BitDeviation"] = var_all;


		root["AdrBoxFull1_ByteDeviation"] = var_all;                                     //����1����
		root["AdrBoxFull1_BitDeviation"] = var_all;


		root["AdrBoxFull2_ByteDeviation"] = var_all;                                     //����2����
		root["AdrBoxFull2_BitDeviation"] = var_all;


		root["AdrBoxFull3_ByteDeviation"] = var_all;                                     //����3����
		root["AdrBoxFull3_BitDeviation"] = var_all;


		root["AdrBoxFull4_ByteDeviation"] = var_all;                                     //����4����
		root["AdrBoxFull4_BitDeviation"] = var_all;


		std::ofstream ofs;
		ofs.open("C://Users//Administrator//Desktop//test1.json");
		ofs << root.toStyledString();
		ofs.close();


		//jsonWriter->write(root, &os);
		//std::string str = os.str();
		return "123";
	}
	bool JsonFunction::WriteJson_mine()
	{
		Json::Value jsonRoot;
		Json::Value jsonItem;
		jsonItem["item1"] = "��һ����Ŀ";
		jsonItem["item2"] = "�ڶ�����Ŀ";
		jsonItem["item3"] = 3;
		jsonRoot.append(jsonItem);

		std::ofstream ofs;
		ofs.open("test1.json");
		ofs << jsonRoot.toStyledString();
		ofs.close();
		return true;
	}
}
