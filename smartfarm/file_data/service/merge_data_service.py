class MergeDataService():
    def __init__(self, user, file_object, column_name):
        self.user = user
        self.file_object = file_object
        self.column_name = column_name
        
    @classmethod    
    def from_serializer(cls, user, serializer):
        return cls(user, serializer.file_object, serializer.validated_data['columnName'])
    
    # def execute(self):
    #     dfs = []
            
    #     for i in range(len(data)):
    #         df = pd.read_json(data.iloc[i,0])
    #         df.rename(columns={column_name[i]:"기준"}, inplace=True)
    #         if type(df['기준']) is not object:
    #             df['기준'] = df['기준'].astype('object')
    #         dfs.append(df)