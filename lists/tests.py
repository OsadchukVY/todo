from django.urls import resolve
from django.test import LiveServerTestCase
from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item, List


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        '''Our GET - request'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')  #

    def test_home_page_returns_correct_html(self):
        """Instead of manually creating an HttpRequest object and calling the view function directly.
        We call self.client.get, passing it the URL we want to test."""
        response = self.client.get('/')
        html = response.content.decode('utf8')  # decode bytes in string of HTML
        self.assertTemplateUsed(response, 'home.html')
        self.assertTrue(html.startswith('<html>'))  # TRUE if our HTML starts with <html>
        self.assertIn('<title>To-Do lists</title>', html)  # Checking if we have  "To-Do lists" in our title
        self.assertTrue(html.strip().endswith('</html>'))  # TRUE if our HTML ends with <html>

    # def test_display_all_items(self):
    #     Item.objects.create(text='Item 1')  # add smth in DB
    #     Item.objects.create(text='Item 2')
    #     response = self.client.get('/lists/the-only-list-in-the-world/')   # get information from request
    #     self.assertContains(response, 'Item 1')     # check item in response
    #     self.assertContains(response, 'Item 2')


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()  # creating List object
        list_.save()  # saving List object

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        # will compare themselves by checking that their primary key (the .id attribute) is the same
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)

    # def test_can_save_a_POST_request(self):
    #     """To do a POST, we call self.client.post,
    #     and as you can see it takes a data argument
    #     which contains the form data we want to send."""
    #     response = self.client.post('/', data={'item_text': 'A new list item'})
    #
    #     self.assertEqual(Item.objects.count(), 1)  # check that one new Item has been saved to the database
    #     new_item = Item.objects.first()  # objects.first() is the same as doing objects.all()[0]
    #     self.assertEqual(new_item.text, 'A new list item')  # check that the item’s text is correct
    #
    # def test_redirects_after_POST(self):
    #
    #     response = self.client.post('/', data={'item_text': 'A new list item'})
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'],
                         correct_list)  # response.context represents the context we’re going to pass into the render function


class NewListTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')


