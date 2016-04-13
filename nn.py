from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD

def create_model():
    #took from keras docs just for the prototype
    model = Sequential()
    model.add(Dense(64, input_dim=42, init='uniform'))
    model.add(Activation('tanh'))
    model.add(Dropout(0.5))
    model.add(Dense(64, init='uniform'))
    model.add(Activation('tanh'))
    model.add(Dropout(0.5))
    model.add(Dense(7, init='uniform'))
    model.add(Activation('softmax'))
    sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd)
    #model.fit(X_train, y_train, nb_epoch=20, batch_size=16, show_accuracy=True)
    #score = model.evaluate(X_test, y_test, batch_size=16)
    return model
