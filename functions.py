def dataframe(input_dict):
    i=0
    if any(input_dict.values()):
        for k,v in input_dict.items():
            if v!='':
                if i==0 :
                    output_data=data[data[k]== v]
                    i=i+1
                else:
                    output_data=output_data[output_data[k]== v]
    else:
        return 'No filter selected'
    output_data=output_data['Owner'].reset_index(drop='index')
    output_data=output_data.to_json()
    return output_data