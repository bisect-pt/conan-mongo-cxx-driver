#include <cstdlib>
#include <iostream>

#include <mongoc.h>
#include <bson.h>
#include <mongocxx/client.hpp>
#include <mongocxx/instance.hpp>
#include <bsoncxx/json.hpp>
#include <bsoncxx/builder/stream/document.hpp>

using namespace bsoncxx;
using namespace mongocxx;

int main()
{
    const mongocxx::instance instance_; // This should be done only once.
    auto conn = mongocxx::client{mongocxx::uri{}};

    bsoncxx::builder::stream::document document{};

    if (false) // compile this don't run it
    {
		auto collection = conn["testdb"]["testcollection"];
		document << "hello" << "world";

		collection.insert_one(document.view());
		auto cursor = collection.find({});

		for (auto&& doc : cursor)
		{
			std::cout << bsoncxx::to_json(doc) << std::endl;
		}
	}

    std::cout << "It works!\n";
    return EXIT_SUCCESS;
}
