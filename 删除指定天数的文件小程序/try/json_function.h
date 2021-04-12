#pragma once
#ifndef JSONFUNCTION_H
#define JSONFUNCTION_H
#include "json/json.h"
#include "json/json-forwards.h"



namespace mine
{


	class JsonFunction
	{
	public:
		JsonFunction();
		~JsonFunction();
		/*bool ParseJson(std::string str, Json::Value &root);*/
		std::string WriteJson(Json::Value &root);
		bool WriteJson_mine();
	private:
		int Cam_ID;
		std::string Control_Signal;
		int ErrorCode;
		int LayerHeight;
		float CaptureFov;
		float CaptureDistance;
		std::string Interface_Client_Address;
		int Interface_Client_Port;
		float CaptureFovRatio;
		float TruckLength;
		float TruckBreadth;
		float CaptureDistanceMargin;


		float var_float;
		int var_all;

	};
}
#endif
