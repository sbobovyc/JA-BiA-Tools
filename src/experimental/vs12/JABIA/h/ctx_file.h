/*
@author: sbobovyc
*/

/*
Copyright (C) 2013 Stanislav Bobovych

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
*/

#ifndef _CTX_FILE_H_
#define _CTX_FILE_H_

#include <map>
#include <vector>
#include <stdint.h>
#include <string>
#include <wchar.h>

class CTX_file {
public:
	int num_items;
	int last_item_id;
	int num_lanugages;
	std::vector<std::string> lang;
	std::map<int, std::wstring> string_map;
	std::map<std::wstring, int> id_map;

	CTX_file() {
		num_items = 0;
		last_item_id = 0;
	};

	CTX_file(void * data_ptr) {
		num_items = *(int *)data_ptr;
		data_ptr = (void *)((int)data_ptr + sizeof(int));
		last_item_id = *(int *)data_ptr;
		data_ptr = (void *)((int)data_ptr + sizeof(int));
		num_lanugages = *(int *)data_ptr;

		data_ptr = (void *)((int)data_ptr + sizeof(int));
		for(int i = 0; i < num_lanugages; i++) {			
			int desc_length = *(int *)data_ptr;
			data_ptr = (void *)((int)data_ptr + sizeof(int));
			std::string description_string = std::string((const char *)data_ptr, desc_length);
			lang.push_back(description_string);
			data_ptr = (void *)((int)data_ptr + sizeof(char)*desc_length);
			uint32_t data_offset =  *(uint32_t *)data_ptr;
			data_ptr = (void *)((int)data_ptr + sizeof(uint32_t));
			//language_map[description_string] = CTX_language();
		}				

		for(int i = 0; i < num_items; i++) {
			int id = *(int *)data_ptr;
			data_ptr = (void *)((int)data_ptr + sizeof(int));
			int item_length = *(int *)data_ptr;
			data_ptr = (void *)((int)data_ptr + sizeof(int));			
			wchar_t * txt = new wchar_t[sizeof(wchar_t)*(2+item_length)];
			ZeroMemory(txt, sizeof(wchar_t)*(2+item_length));
			memcpy(txt, data_ptr, sizeof(wchar_t)*(item_length));
			std::wstring item_text = std::wstring(txt);
			string_map[id] = item_text;
			id_map[item_text] = id;
			data_ptr = (void *)((int)data_ptr + sizeof(wchar_t)*item_length);
		}
	};
};

class CTX_language {
public:
	uint32_t data_offset;
	std::map<int, std::string> data;
};

#endif /* _CTX_FILE_H_ */