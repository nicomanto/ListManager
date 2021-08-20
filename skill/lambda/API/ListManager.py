class ListManager:
    def __init__(self, handler_input, listName):
        self.listManagementService = handler_input.service_client_factory.get_list_management_service()
        listOfLists = self.listManagementService.get_lists_metadata().to_dict()[
            'lists']

        found = False
        for l in listOfLists:
            if found:
                break

            if(l['name'] == listName):
                found = True
                self.listID = l['list_id']

        if not found:
            raise ValueError('List not present')

    def getListItem(self):
        return self.listManagementService.get_list(self.listID, 'active').to_dict()['items']
