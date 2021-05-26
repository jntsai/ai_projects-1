{"metadata":{"kernelspec":{"language":"python","display_name":"Python 3","name":"python3"},"language_info":{"pygments_lexer":"ipython3","nbconvert_exporter":"python","version":"3.6.4","file_extension":".py","codemirror_mode":{"name":"ipython","version":3},"name":"python","mimetype":"text/x-python"}},"nbformat_minor":4,"nbformat":4,"cells":[{"cell_type":"code","source":"# %% [code] {\"execution\":{\"iopub.status.busy\":\"2021-05-26T05:22:39.374191Z\",\"iopub.execute_input\":\"2021-05-26T05:22:39.374518Z\",\"iopub.status.idle\":\"2021-05-26T05:22:44.677520Z\",\"shell.execute_reply.started\":\"2021-05-26T05:22:39.374489Z\",\"shell.execute_reply\":\"2021-05-26T05:22:44.676686Z\"}}\n\n# Import the necessary libs\nimport numpy as np\nimport matplotlib.pyplot as plt\n\nnp.random.seed(2) #! to generate the same random numbers everytime we run the script\n\nfrom sklearn.model_selection import train_test_split\nimport tensorflow as tf\n\nfrom keras.models import Sequential\nfrom keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D, BatchNormalization\nfrom keras.optimizers import RMSprop\nfrom keras.preprocessing.image import ImageDataGenerator\n\n# %% [markdown]\n# ## Shuffle & Split the dataset\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2021-05-26T05:41:00.142312Z\",\"iopub.execute_input\":\"2021-05-26T05:41:00.142724Z\",\"iopub.status.idle\":\"2021-05-26T05:41:00.681690Z\",\"shell.execute_reply.started\":\"2021-05-26T05:41:00.142689Z\",\"shell.execute_reply\":\"2021-05-26T05:41:00.679665Z\"}}\n#! keras has the dataset already preprocessed so we can use it directly\n(imgs_train, labels_train), (imgs_test, labels_test) = tf.keras.datasets.mnist.load_data()\n\n# Preprocess the data (these are NumPy arrays)\nimgs_train = imgs_train.reshape(-1,28,28,1).astype(\"float32\") / 255\nimgs_test = imgs_test.reshape(-1,28,28,1).astype(\"float32\") / 255\n\nlabels_train = labels_train.astype(\"float32\")\nlabels_test = labels_test.astype(\"float32\")\n\n#! splitt and shuffle the data sothat the test data is 30% of the whole data\nx_train, x_val, y_train, y_val = train_test_split(imgs_train, labels_train, test_size=0.3)\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2021-05-26T05:39:00.063726Z\",\"iopub.execute_input\":\"2021-05-26T05:39:00.064072Z\",\"iopub.status.idle\":\"2021-05-26T05:39:00.071285Z\",\"shell.execute_reply.started\":\"2021-05-26T05:39:00.064042Z\",\"shell.execute_reply\":\"2021-05-26T05:39:00.069886Z\"}}\n\ndef show_img(x_data, y_data, index, show_axis='off', cmap=\"gray\"):\n    plt.axis(show_axis)\n    plt.suptitle(y_data[index], fontsize=20)\n    plt.imshow(x_data[index][...,0],  cmap=cmap)\n    \n    \n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2021-05-26T05:39:00.790917Z\",\"iopub.execute_input\":\"2021-05-26T05:39:00.791247Z\",\"iopub.status.idle\":\"2021-05-26T05:39:00.846120Z\",\"shell.execute_reply.started\":\"2021-05-26T05:39:00.791215Z\",\"shell.execute_reply\":\"2021-05-26T05:39:00.845275Z\"}}\nshow_img(x_train, y_train, 14301)\n\n# %% [markdown]\n# ## Augmenting the Images\n# we will apply this get get more images for traning by applying some image processing techniques\n# like zooming, shifting, etc...\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2021-05-26T05:41:06.410485Z\",\"iopub.execute_input\":\"2021-05-26T05:41:06.410859Z\",\"iopub.status.idle\":\"2021-05-26T05:41:06.466733Z\",\"shell.execute_reply.started\":\"2021-05-26T05:41:06.410827Z\",\"shell.execute_reply\":\"2021-05-26T05:41:06.465919Z\"}}\n\n\ndatagen = ImageDataGenerator(\n        zoom_range = 0.1, # Randomly zoom image \n        width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)\n        height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)\n        horizontal_flip=False,  # don't flip images\n        vertical_flip=False, # don't flip images\n) \n\n\ndatagen.fit(x_train)\n\n\n\n# %% [markdown]\n# # Create the model\n\n# %% [markdown]\n# ## Design the model\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2021-05-26T05:42:20.947649Z\",\"iopub.execute_input\":\"2021-05-26T05:42:20.947980Z\",\"iopub.status.idle\":\"2021-05-26T05:42:21.128551Z\",\"shell.execute_reply.started\":\"2021-05-26T05:42:20.947949Z\",\"shell.execute_reply\":\"2021-05-26T05:42:21.127787Z\"}}\nmodel = Sequential([\n        # -------------- Convolution Layers --------------\n\n        # First CONV\n        Conv2D(64, (3,3), activation=\"relu\", input_shape=(28,28,1), padding=\"same\",),\n        MaxPool2D((2,2)),\n        BatchNormalization(),\n\n        # Second CONV\n        Conv2D(64, (3,3), activation=\"relu\", padding=\"same\",),\n        BatchNormalization(),\n        MaxPool2D((2,2)),\n        Dropout(0.3),\n\n        # Third CONV\n        Conv2D(128, (3,3), activation=\"relu\", padding=\"same\",),\n        BatchNormalization(),\n        MaxPool2D((2,2)),\n        MaxPool2D((2,2), strides=(2,2)),\n        Dropout(0.3),\n\n\n        # -------------- Fully Connected Layers --------------\n        Flatten(),\n        Dense(256, activation=\"relu\"),\n        BatchNormalization(),\n        Dropout(0.3),\n\n\n        # Output Layer we will predict 10 numbers from 0 to 9\n        Dense(10, activation=\"softmax\"),\n\n])\n\n\n\n## Compile the model\noptimizer = RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)\nloss = \"sparse_categorical_crossentropy\"\nmodel.compile(optimizer = optimizer , loss = loss, metrics=[\"acc\"])\n\n\n# %% [markdown]\n# ## Start Model Training\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2021-05-26T05:42:40.029259Z\",\"iopub.execute_input\":\"2021-05-26T05:42:40.029658Z\",\"iopub.status.idle\":\"2021-05-26T05:42:40.037014Z\",\"shell.execute_reply.started\":\"2021-05-26T05:42:40.029587Z\",\"shell.execute_reply\":\"2021-05-26T05:42:40.035865Z\"}}\nclass myCallback(tf.keras.callbacks.Callback): \n    def on_epoch_end(self, epoch, logs={}):\n        # keep track of the validation accuracy and if it reaches high accuracy like 99%\n        if(logs.get('val_acc') >= 0.99):\n            print(\"\\nReached 99% accuracy so cancelling training!\")\n            self.model.stop_training = True\n        \n\ncallbacks = myCallback()\n\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2021-05-26T05:42:42.808893Z\",\"iopub.execute_input\":\"2021-05-26T05:42:42.809218Z\",\"iopub.status.idle\":\"2021-05-26T05:44:37.004992Z\",\"shell.execute_reply.started\":\"2021-05-26T05:42:42.809187Z\",\"shell.execute_reply\":\"2021-05-26T05:44:37.004265Z\"}}\nepochs = 32 # Turn epochs to 30 to get 0.9967 accuracy\nbatch_size = 256 #64,128 ,256,512 \n\nwith tf.device(\"/GPU:0\"):\n\n    #Prediction model\n    history = model.fit_generator(\n        datagen.flow(x_train,y_train, batch_size=batch_size),\n        epochs = epochs,\n        validation_data = (x_val,y_val),\n        verbose = 1, \n        steps_per_epoch=x_train.shape[0] // batch_size,\n        callbacks=[callbacks]\n    )\n\n\n# %% [markdown]\n# ## Save the model\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2021-05-26T05:44:42.699816Z\",\"iopub.execute_input\":\"2021-05-26T05:44:42.700133Z\",\"iopub.status.idle\":\"2021-05-26T05:44:45.710087Z\",\"shell.execute_reply.started\":\"2021-05-26T05:44:42.700103Z\",\"shell.execute_reply\":\"2021-05-26T05:44:45.709133Z\"}}\nmodel.save('english_digits_model')  # creates a pb file (Saved model)\n!zip -r eng.zip \"./english_digits_model\"\n\n\n# %% [markdown]\n# ## Test\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2021-05-26T05:44:47.418077Z\",\"iopub.execute_input\":\"2021-05-26T05:44:47.418412Z\",\"iopub.status.idle\":\"2021-05-26T05:44:47.474425Z\",\"shell.execute_reply.started\":\"2021-05-26T05:44:47.418378Z\",\"shell.execute_reply\":\"2021-05-26T05:44:47.473403Z\"}}\nshow_img(x_train, y_train, 1555)\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2021-05-26T05:45:28.972441Z\",\"iopub.execute_input\":\"2021-05-26T05:45:28.972798Z\",\"iopub.status.idle\":\"2021-05-26T05:45:29.016274Z\",\"shell.execute_reply.started\":\"2021-05-26T05:45:28.972767Z\",\"shell.execute_reply\":\"2021-05-26T05:45:29.015319Z\"}}\nprint(model.predict(x_train[1555].reshape(1,28,28,1)).argmax())","metadata":{"_uuid":"ee65bf19-0098-4148-9ab1-0119ebe1733c","_cell_guid":"9311d5d8-88f3-40f5-94e5-6785145e3faf","collapsed":false,"jupyter":{"outputs_hidden":false},"trusted":true},"execution_count":null,"outputs":[]}]}