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
		root["Cam_ID"] = Cam_ID;                                            //相机ID
		root["Interface_Client_Address"] = Interface_Client_Address;         // 图像处理客户端地址
		root["Interface_Client_Port"] = Interface_Client_Port;               //图像处理客户端端口
		root["Control_Signal"] = Control_Signal;                            //控制信号：开始、暂停、停止、参数保存
		root["ErrorCode"] = ErrorCode;                                      //错误代码
		root["LayerHeight"] = LayerHeight;                                  //当前层高
		root["CaptureFov"] = CaptureFov;                                    // 当前视场
		root["CaptureDistance"] = CaptureDistance;                          //拍照间隔
		root["CaptureFovRatio"] = CaptureFovRatio;                            // 拍照视场的比率
		root["TruckLength"] = TruckLength;                                    // 车长
		root["TruckBreadth"] = TruckBreadth;                                  //车宽
		root["CaptureDistanceMargin"] = CaptureDistanceMargin;                // 拍照间隔的扩大值
		root["TruckCornerPoint1_x"] = var_float;                        // 汽车的角点1
		root["TruckCornerPoint1_y"] = var_float;                        // 汽车的角点1

		root["TruckCornerPoint2_x"] = var_float;                        // 汽车的角点2
		root["TruckCornerPoint2_y"] = var_float;                        // 汽车的角点2

		root["TruckCornerPoint3_x"] = var_float;                        // 汽车的角点3
		root["TruckCornerPoint3_y"] = var_float;                        // 汽车的角点3

		root["TruckCornerPoint4_x"] = var_float;                        // 汽车的角点4
		root["TruckCornerPoint4_y"] = var_float;                        // 汽车的角点4

		root["SafePos_x"] = var_float;                                            //安全点,固定值，作为设置参数写死
		root["SafePos_y"] = var_float;                                            //安全点,固定值，作为设置参数写死
		root["SafePos_z"] = var_float;                                            //安全点,固定值，作为设置参数写死
		root["SafePos_c"] = var_float;                                            //安全点,固定值，作为设置参数写死

		root["ReCheckPos_x"] = var_float;                                       //二次定位点，固定值，作为设置参数写死
		root["ReCheckPos_y"] = var_float;                                       //二次定位点，固定值，作为设置参数写死
		root["ReCheckPos_z"] = var_float;                                       //二次定位点，固定值，作为设置参数写死
		root["ReCheckPos_c"] = var_float;                                       //二次定位点，固定值，作为设置参数写死

		root["BoxRefPoint1_x"] = var_float;                                   // 料框1坐标系原点
		root["BoxRefPoint1_y"] = var_float;                                   // 料框1坐标系原点
		root["BoxRefPoint1_z"] = var_float;                                   // 料框1坐标系原点
		root["BoxRefPoint1_c"] = var_float;                                   // 料框1坐标系原点

		root["BoxRefPoint2_x"] = var_float;                                   // 料框2 坐标系原点
		root["BoxRefPoint2_y"] = var_float;                                   // 料框2 坐标系原点
		root["BoxRefPoint2_z"] = var_float;                                   // 料框2 坐标系原点
		root["BoxRefPoint2_c"] = var_float;                                   // 料框2 坐标系原点


		//2 实时分析
		root["CapturePointCurrent_x"] = var_float;     //当前拍照点
		root["CapturePointCurrent_y"] = var_float;     //当前拍照点

		root["PickPosCurrent_x"] = var_float;                                //当前抓取点
		root["PickPosCurrent_y"] = var_float;                                //当前抓取点
		root["PickPosCurrent_z"] = var_float;                                //当前抓取点
		root["PickPosCurrent_c"] = var_float;                                //当前抓取点

		root["BoxLength"] = var_float;                                           //包裹长
		root["BoxBreadth"] = var_float;                                        //包裹宽
		root["Pos_queue_x"] = var_float;                                           //抓取点位置序列
		root["Pos_queue_y"] = var_float;                                           //抓取点位置序列
		root["Pos_queue_z"] = var_float;                                           //抓取点位置序列
		root["Pos_queue_c"] = var_float;                                           //抓取点位置序列
		root["CapturePoint_x"] = var_float;                                     //拍照点序列
		root["CapturePoint_y"] = var_float;                                     //拍照点序列



		//3 plc地址
														   //主臂机器人ID
		root["AdrActPos_ByteDeviation"] = var_all;                                     //当前位置
		root["AdrActPos_BitDeviation"] = var_all;

		root["AdrPickPos_ByteDeviation"] = var_all;                                     //抓取位置
		root["AdrPickPos_BitDeviation"] = var_all;

		root["AdrPlacePos_ByteDeviation"] = var_all;                                     //放置位置
		root["AdrPlacePos_BitDeviation"] = var_all;

		root["AdrState_ByteDeviation"] = var_all;                                     //状态
		root["AdrState_BitDeviation"] = var_all;

		root["TransitionPoint1_ByteDeviation"] = var_all;                                     //过渡点1
		root["TransitionPoint1_BitDeviation"] = var_all;

		root["TransitionPoint2_ByteDeviation"] = var_all;                                     //过渡点2
		root["TransitionPoint2_BitDeviation"] = var_all;


		//4 plcdata address		

		root["AdrCapPos_ByteDeviation"] = var_all;                                         //当前位置	
		root["AdrCapPos_BitDeviation"] = var_all;


		root["AdrReCheckPos_ByteDeviation"] = var_all;                                     //放置位置
		root["AdrReCheckPos_BitDeviation"] = var_all;


		root["CylinderPos1_ByteDeviation"] = var_all;                                     //气缸1位置
		root["CylinderPos1_BitDeviation"] = var_all;


		root["CylinderPos2_ByteDeviation"] = var_all;                                     //气缸2位置
		root["CylinderPos2_BitDeviation"] = var_all;
		// DI


		root["AdrCarInPosition_ByteDeviation"] = var_all;                                     //停车到位信号
		root["AdrCarInPosition_BitDeviation"] = var_all;


		root["bVacuum_ByteDeviation"] = var_all;                                     //真空开关信号
		root["bVacuum_BitDeviation"] = var_all;


		root["AdrEmptyBox1_ByteDeviation"] = var_all;                                     //笼车1清空
		root["AdrEmptyBox1_BitDeviation"] = var_all;


		root["AdrEmptyBox2_ByteDeviation"] = var_all;                                     //笼车2清空
		root["AdrEmptyBox2_BitDeviation"] = var_all;


		root["AdrEmptyBox3_ByteDeviation"] = var_all;                                     //笼车3清空
		root["AdrEmptyBox3_BitDeviation"] = var_all;


		root["AdrEmptyBox4_ByteDeviation"] = var_all;                                     //笼车4清空
		root["AdrEmptyBox4_BitDeviation"] = var_all;


		//DO
		root["AdrSuckerStart_ByteDeviation"] = var_all;                                 //吸盘开关
		root["AdrSuckerStart_BitDeviation"] = var_all;


		root["AdrBoxFull1_ByteDeviation"] = var_all;                                     //笼车1码满
		root["AdrBoxFull1_BitDeviation"] = var_all;


		root["AdrBoxFull2_ByteDeviation"] = var_all;                                     //笼车2码满
		root["AdrBoxFull2_BitDeviation"] = var_all;


		root["AdrBoxFull3_ByteDeviation"] = var_all;                                     //笼车3码满
		root["AdrBoxFull3_BitDeviation"] = var_all;


		root["AdrBoxFull4_ByteDeviation"] = var_all;                                     //笼车4码满
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
		jsonItem["item1"] = "第一个条目";
		jsonItem["item2"] = "第二个条目";
		jsonItem["item3"] = 3;
		jsonRoot.append(jsonItem);

		std::ofstream ofs;
		ofs.open("test1.json");
		ofs << jsonRoot.toStyledString();
		ofs.close();
		return true;
	}
}
