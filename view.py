from tkinter import *


class View:
    # Completed analysis count keep tracks of the number of models that have finished analysing an article.
    completed_analysis_count = 0

    root = Tk()

    analyse_button = None
    analyse_button_text = StringVar()

    article_text = None
    selected_option = None
    summary_text = None

    min_parameter_label = None
    max_parameter_label = None
    min_parameter_label_text = StringVar()
    max_parameter_label_text = StringVar()
    min_parameter_input = None
    max_parameter_input = None

    sentiment_text = StringVar()
    confidence_text = StringVar()

    person_text = StringVar()
    organisation_text = StringVar()
    location_text = StringVar()
    misc_text = StringVar()

    article_word_count = StringVar()
    summary_word_count = StringVar()

    def __init__(self):
        """
        Set title of window screen.
        """
        self.root.title("Text Analyser")

        """
        Disable maximise option.
        """
        self.root.resizable(0, 0)

        """
        Set icon.
        """
        self.root.iconbitmap("icon.ico")

        """
        Define root canvas.
        """
        canvas = Canvas(self.root, bg="pink")
        canvas.grid(columnspan=2, rowspan=1)

        """
        Separate UI into left canvas and right canvas.
        """
        left_canvas = Canvas(canvas, bg="red")
        left_canvas.grid(column=0, row=0)

        right_canvas = Canvas(canvas, bg="blue")
        right_canvas.grid(column=1, row=0, sticky=NSEW)

        """
        Initialise article text widget.
        """
        self.article_text = Text(left_canvas, height=40, width=70, wrap=WORD)
        self.article_text.insert("1.0", "Insert an article to analyse...")
        self.article_text.grid(column=0, row=0, padx=20, pady=20)

        """
        Initialise the dropdown widget that allows the user to reduce the length of the article by percentage or word 
        count.
        """
        option_menu_canvas = Canvas(left_canvas, bg="purple")
        option_menu_canvas.grid(column=0, row=1, padx=20, sticky=W)

        option_menu = Canvas(option_menu_canvas, bg="green")
        Label(option_menu, text="Summarise the article by").pack(padx=(5, 0), side="left")

        options = ["PERCENTAGE", "WORD COUNT"]
        option_text = StringVar()
        option_text.set(options[0])
        self.selected_option = options[0]

        dropdown = OptionMenu(option_menu, option_text, *options, command=self.set_option)
        dropdown.pack(padx=(20, 0), side="right")

        option_menu.pack()

        """
        This ensures that the values entered into the parameters are digits/
        """

        def parameters_callback(text):
            if str.isdigit(text) or text == "":
                return True
            else:
                return False

        validate = self.root.register(parameters_callback)

        """
        Initialise the minimum and maximum parameters.
        """
        parameters_canvas = Canvas(left_canvas, bg="purple")
        parameters_canvas.grid(column=0, row=2, columnspan=2, rowspan=2, padx=20, pady=20, sticky=W)

        self.min_parameter_label = Label(parameters_canvas, textvariable=self.min_parameter_label_text)
        self.min_parameter_label.grid(column=0, row=0, padx=5, pady=5)

        self.min_parameter_input = Entry(parameters_canvas, validate='all', validatecommand=(validate, '%P'))
        self.min_parameter_input.grid(column=1, row=0, padx=5, pady=5)

        self.max_parameter_label = Label(parameters_canvas, textvariable=self.max_parameter_label_text)
        self.max_parameter_label.grid(column=0, row=1, padx=5, pady=5)

        self.max_parameter_input = Entry(parameters_canvas, validate='all', validatecommand=(validate, '%P'))
        self.max_parameter_input.grid(column=1, row=1, padx=5, pady=5)

        self.initialise_percentage_parameters()

        """
        Initialise analyse button.
        """
        self.analyse_button = Button(left_canvas, textvariable=self.analyse_button_text, width=15, bg="yellow")
        self.analyse_button.grid(column=0, row=4, pady=(0, 20), sticky=NS)
        self.analyse_button_text.set("ANALYSE")

        """
        Initialise summary text widget.
        """
        Label(right_canvas, text="Summary").grid(column=1, row=0, padx=(20, 0), pady=(20, 0), sticky=W)

        self.summary_text = Text(right_canvas, height=25, width=70, wrap=WORD)
        self.summary_text.grid(column=1, row=1, padx=20, pady=20)

        """
        Initialise sentiment section.
        """
        sentiment_canvas = Canvas(right_canvas, bg="green")
        sentiment_canvas.grid(column=0, row=2, columnspan=2, rowspan=2, padx=20, pady=(0, 20), sticky=W)

        sentiment_label_1 = Label(sentiment_canvas, text="Sentiment")
        sentiment_label_1.grid(column=0, row=0, padx=5, pady=5, sticky=W)

        sentiment_label_2 = Label(sentiment_canvas, textvariable=self.sentiment_text, width=15)
        sentiment_label_2.grid(column=1, row=0, padx=5, pady=5)

        confidence_label_1 = Label(sentiment_canvas, text="Confidence")
        confidence_label_1.grid(column=0, row=1, padx=5, pady=5, sticky=W)

        confidence_label_2 = Label(sentiment_canvas, textvariable=self.confidence_text, width=15)
        confidence_label_2.grid(column=1, row=1, padx=5, pady=5)

        """
        Initialise entity section.
        """
        entity_canvas = Canvas(right_canvas, bg="purple")
        entity_canvas.grid(column=0, row=4, columnspan=2, rowspan=4, padx=20, pady=(0, 20), sticky=W)

        person_label_1 = Label(entity_canvas, text="Persons")
        person_label_1.grid(column=0, row=0, padx=5, pady=5, sticky=W)

        person_label_2 = Label(entity_canvas, textvariable=self.person_text, width=60, anchor="w")
        person_label_2.grid(column=1, row=0, padx=5, pady=5, sticky=W)

        organisation_label_1 = Label(entity_canvas, text="Organisations")
        organisation_label_1.grid(column=0, row=1, padx=5, pady=5, sticky=W)

        organisation_label_2 = Label(entity_canvas, textvariable=self.organisation_text, width=60, anchor="w")
        organisation_label_2.grid(column=1, row=1, padx=5, pady=5, sticky=W)

        location_label_1 = Label(entity_canvas, text="Locations")
        location_label_1.grid(column=0, row=2, padx=5, pady=5, sticky=W)

        organisation_label_2 = Label(entity_canvas, textvariable=self.location_text, width=60, anchor="w")
        organisation_label_2.grid(column=1, row=2, padx=5, pady=5, sticky=W)

        misc_label_1 = Label(entity_canvas, text="Miscellaneous")
        misc_label_1.grid(column=0, row=3, padx=5, pady=5, sticky=W)

        misc_label_2 = Label(entity_canvas, textvariable=self.misc_text, width=60, anchor="w")
        misc_label_2.grid(column=1, row=3, padx=5, pady=5, sticky=W)

        """
        Initialise statistics section.
        """
        stats_canvas = Canvas(right_canvas, bg="red")
        stats_canvas.grid(column=0, row=9, columnspan=2, rowspan=2, padx=20, pady=(0, 20), sticky=W)

        article_wc_label_1 = Label(stats_canvas, text="Article word count")
        article_wc_label_1.grid(column=0, row=0, padx=5, pady=5, sticky=W)

        article_wc_label_2 = Label(stats_canvas, textvariable=self.article_word_count, width=20, anchor="w")
        article_wc_label_2.grid(column=1, row=0, padx=5, pady=5)

        summary_wc_label_1 = Label(stats_canvas, text="Summary word count")
        summary_wc_label_1.grid(column=0, row=1, padx=5, pady=5, sticky=W)

        summary_wc_label_2 = Label(stats_canvas, textvariable=self.summary_word_count, width=20, anchor="w")
        summary_wc_label_2.grid(column=1, row=1, padx=5, pady=5)

    def initialise_percentage_parameters(self):
        self.min_parameter_label_text.set("Minimum percentage")
        self.max_parameter_label_text.set("Maximum percentage")

        self.update_entry_widget_text(self.min_parameter_input, "30")
        self.update_entry_widget_text(self.max_parameter_input, "50")

    def initialise_word_count_parameters(self):
        self.min_parameter_label_text.set("Minimum word count")
        self.max_parameter_label_text.set("Maximum word count")

        self.update_entry_widget_text(self.min_parameter_input, "150")
        self.update_entry_widget_text(self.max_parameter_input, "200")

    def model_completed_analysis(self):
        self.completed_analysis_count += 1

        if self.completed_analysis_count == 3:
            self.completed_analysis_count = 0
            self.enable_analyse_button()

    def disable_analyse_button(self):
        self.analyse_button.configure(state=DISABLED)
        self.analyse_button_text.set("LOADING...")

    def enable_analyse_button(self):
        self.analyse_button.configure(state=NORMAL)
        self.analyse_button_text.set("ANALYSE")

    def get_article(self):
        return self.article_text.get("1.0", END).strip()

    def set_option(self, text):
        self.selected_option = text

        if text == "PERCENTAGE":
            self.initialise_percentage_parameters()
        else:
            self.initialise_word_count_parameters()

    def get_option(self):
        return self.selected_option

    def get_min_parameter(self):
        return int(self.min_parameter_input.get())

    def get_max_parameter(self):
        return int(self.max_parameter_input.get())

    def set_summary(self, text):
        self.summary_text.delete("1.0", END)
        self.summary_text.insert("1.0", text)

    def set_sentiment(self, text):
        self.sentiment_text.set(text)

    def set_confidence(self, text):
        self.confidence_text.set(text)

    def set_person(self, text):
        self.person_text.set(text)

    def set_organisation(self, text):
        self.organisation_text.set(text)

    def set_location(self, text):
        self.location_text.set(text)

    def set_misc(self, text):
        self.misc_text.set(text)

    def set_article_word_count(self, text):
        self.article_word_count.set(text)

    def set_summary_word_count(self, text):
        self.summary_word_count.set(text)

    def run(self):
        self.root.mainloop()

    @staticmethod
    def update_entry_widget_text(entry_widget: Entry, text: str, state=NORMAL):
        entry_widget.delete(0, END)
        entry_widget.insert(0, text)
        entry_widget.configure(state=state)
