RAW_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Webscraper Test Page</title>
</head>
<body>
    <h1>Welcome to the Webscraper Test Page</h1>
    <p>This page contains various elements for scraping practice.</p>

    <h2>Links</h2>
    <ul>
        <li><a href="https://example.com">Example Website</a></li>
        <li><a href="https://sample.com">Sample Website</a></li>
        <li><a href="https://test.com">Test Website</a></li>
    </ul>

    <h2>Products</h2>
    <table border="1">
        <tr>
            <th>Product</th>
            <th>Price</th>
            <th>Availability</th>
        </tr>
        <tr>
            <td>Widget A</td>
            <td>$10.99</td>
            <td>In Stock</td>
        </tr>
        <tr>
            <td>Widget B</td>
            <td>$23.50</td>
            <td>Out of Stock</td>
        </tr>
        <tr>
            <td>Widget C</td>
            <td>$5.75</td>
            <td>In Stock</td>
        </tr>
    </table>

    <h2>Images</h2>
    <img src="https://via.placeholder.com/150" alt="Placeholder Image 1">
    <img src="https://via.placeholder.com/100" alt="Placeholder Image 2">

    <h2>Articles</h2>
    <div class="article">
        <h3>Article One</h3>
        <p>Author: Alice</p>
        <p>This is the first article content.</p>
    </div>
    <div class="article">
        <h3>Article Two</h3>
        <p>Author: Bob</p>
        <p>This is the second article content.</p>
    </div>
</body>
</html>
"""

from scrapegoat_core import Gardener
from unittest import TestCase, main

class TestHTMLToNodes(TestCase):
	def __init__(self, methodName = "runTest"):
		super().__init__(methodName)
		self.gardener: Gardener = None

	def setUp(self):
		self.gardener = Gardener()
		self.tree = self.gardener.grow_tree(RAW_HTML)
		return super().setUp()

	def test_number_of_children(self):
		self.assertEqual(len(self.tree.children), 2) # <html> has <head> and <body>
		self.assertEqual(len(self.tree.children[0].children), 2) # <head> has <meta> and <title>
		self.assertEqual(len(self.tree.children[1].children), 12) # <body> has 1 <h1>, 4 <h2>, 1 <p>, 1 <ul>, 1 <table>, 2 <img>, 2 <div>
		self.assertEqual(len(self.tree.children[1].children[3].children), 3) # <ul> has 3 <li>
		self.assertEqual(len(self.tree.children[1].children[11].children), 3) # last <div> has 2 <p> and 1 <h3>
	
	def test_type_of_nodes(self):
		self.assertEqual(self.tree.tag_type, "html") # 1st node is <html>

		body_node_types = [node.tag_type for node in self.tree.children[1].children]
		expected_types = ["h1", "p", "h2", "ul", "h2", "table", "h2", "img", "img", "h2", "div", "div"]
		self.assertCountEqual(body_node_types, expected_types)

		last_div_node_types = [node.tag_type for node in self.tree.children[1].children[11].children]
		expected_last_div_types = ["h3", "p", "p"]
		self.assertCountEqual(last_div_node_types, expected_last_div_types)

	def test_retrieval_instructions(self):
		self.assertEqual(self.tree.retrieval_instructions, "SCRAPE 1 html IN POSITION=1;")

		body_retrieval_instructions = [node.retrieval_instructions for node in self.tree.children[1].children]
		expected_retrieval_instructions = ["SCRAPE 1 h1 IN POSITION=1;", "SCRAPE 1 p IN POSITION=1;", "SCRAPE 1 h2 IN POSITION=1;", "SCRAPE 1 ul IN POSITION=1;", "SCRAPE 1 h2 IN POSITION=2;", "SCRAPE 1 table IN POSITION=1;", "SCRAPE 1 h2 IN POSITION=3;", "SCRAPE 1 img IN POSITION=1;", "SCRAPE 1 img IN POSITION=2;", "SCRAPE 1 h2 IN POSITION=4;", "SCRAPE 1 div IN POSITION=1;", "SCRAPE 1 div IN POSITION=2;"]
		self.assertCountEqual(body_retrieval_instructions, expected_retrieval_instructions)

if __name__ == '__main__':
		main()